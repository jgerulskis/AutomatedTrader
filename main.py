import requests
from requests_oauthlib import OAuth1
import pandas as pd
import time
import config

base_url = 'https://api.twitter.com/'
auth_url = '{}oauth2/token'.format(base_url)
auth_resp = OAuth1(config.consumer_key, config.secret_consumer_key, config.access_key, config.secret_access_key)

csv_file = config.data_path

def search(search_term="bitcoin", MAX_RESULTS=100):
    url = 'https://api.twitter.com/2/tweets/search/recent?query=' + search_term + '&tweet.fields=created_at,public_metrics,lang&user.fields=public_metrics&max_results=' + str(MAX_RESULTS)
    search_results = requests.get(url, auth=auth_resp)
    print('Server responded with {}'.format(search_results.status_code))
    print(search_results.text)
    if (search_results.status_code == 200):
        data = search_results.json().get('data')
        print('Got {} tweets'.format(len(data)))
        return data
    else:
        print('Error on request!')
        return None

def append_data(json_list):
    df = pd.DataFrame.from_records(json_list)
    export_csv = df.to_csv(csv_file, mode='a')
    print('Exported to ' + csv_file)

"""
The Twitter API allows 500,000 requests per a month

500,000 tweets a month
~16,665  tweets a day
~694     tweets an hour
~11      tweets a minute
"""
total_tweets = 0
total_time = 0
while (True):
    print('\t Total tweets: ' + str(total_tweets))
    print('\t Total time: ' + str(total_time))
    data = search(MAX_RESULTS=11)
    if (data != None):
        total_tweets = len(data)
        append_data(data)
    time.sleep(60)
    total_time += 60