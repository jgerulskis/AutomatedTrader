import requests
import os
import json
import config

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


class TwitterStream:
    def __init__(self, bearer_token, timeframe=60, verbose=True):
        self.verbose = verbose
        self.bearer_token = bearer_token
        self.timeframe = timeframe
        self.headers = None
        if self.verbose:
            print("Resetting rules")
        self.resetRules()
        if (self.verbose):
           print("Ready to start")

    def start(self):
      analyzer = SentimentIntensityAnalyzer()
      self.get_stream(set, analyzer)

    def resetRules(self):
        self.headers = self.create_headers()
        rules = self.get_rules()
        delete = self.delete_all_rules(rules)
        set = self.set_rules(delete)

    def create_headers(self):
        headers = {"Authorization": "Bearer {}".format(self.bearer_token)}
        return headers

    def get_rules(self):
        response = requests.get(
            "https://api.twitter.com/2/tweets/search/stream/rules", headers=self.headers
        )
        if response.status_code != 200:
            raise Exception(
                "Cannot get rules (HTTP {}): {}".format(
                    response.status_code, response.text)
            )
        return response.json()

    def delete_all_rules(self, rules):
        if rules is None or "data" not in rules:
            return None

        ids = list(map(lambda rule: rule["id"], rules["data"]))
        payload = {"delete": {"ids": ids}}
        response = requests.post(
            "https://api.twitter.com/2/tweets/search/stream/rules",
            headers=self.headers,
            json=payload
        )
        if response.status_code != 200:
            raise Exception(
                "Cannot delete rules (HTTP {}): {}".format(
                    response.status_code, response.text
                )
            )

    def set_rules(self, delete):
        sample_rules = [
            {"value": "#Eth Ethereum lang:en"}
        ]
        payload = {"add": sample_rules}
        response = requests.post(
            "https://api.twitter.com/2/tweets/search/stream/rules",
            headers=self.headers,
            json=payload,
        )
        if response.status_code != 201:
            raise Exception(
                "Cannot add rules (HTTP {}): {}".format(
                    response.status_code, response.text)
            )

    def get_stream(self, set, analyzer):
        response = requests.get(
            "https://api.twitter.com/2/tweets/search/stream", headers=self.headers, stream=True,
        )
        if self.verbose:
            print("Connected to stream with status code {}".format(
            response.status_code))
        if response.status_code != 200:
            raise Exception(
                "Cannot get stream (HTTP {}): {}".format(
                    response.status_code, response.text
                )
            )
        for response_line in response.iter_lines():
            if response_line:
                json_response = json.loads(response_line)
                text = json_response['data']['text']
                score = analyzer.polarity_scores(text)
                if self.verbose:
                    print("{:-<65} {}".format(text, str(score)))


