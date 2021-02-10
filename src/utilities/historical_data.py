import requests
from requests_oauthlib import OAuth1
import pandas as pd
import time
import config
import progressbar

from data_point import DataPoint
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


class TwitterHistorical():
  def __init__(self, consumer_key, secret_consumer_key, access_key, secret_access_key, out_path, verbose=True):
    self.verbose = verbose
    if (self.verbose):
      print("Authenticating")
    self.auth_resp = OAuth1(consumer_key, secret_consumer_key, access_key, secret_access_key)
    self.csv_file = out_path
    if (self.verbose):
      print("Ready to start")

  def search(self, MAX_RESULTS=100):
      search_term = "Ether"
      url = 'https://api.twitter.com/2/tweets/search/recent?query=' + search_term + '&tweet.fields=created_at,public_metrics,lang&user.fields=public_metrics&max_results=' + str(MAX_RESULTS)
      search_results = requests.get(url, auth=self.auth_resp)
      if self.verbose:
        print('Server responded with {}'.format(search_results.status_code))
        print(search_results.text)
      if (search_results.status_code == 200):
          data = search_results.json().get('data')
          return data
      else:
          print('Error on request!')
          return None

  def append_data(self, json_list):
      df = pd.DataFrame.from_records(json_list)
      df.to_csv(self.csv_file, mode='a')
      if (self.verbose):
        print('Exported to ' + self.csv_file)

  def start(self, tpm=11):
    """
    tpm - Tweets per minute

    Our API license allows 500,000 requests a month

    500,000 tweets a month
    ~16,665  tweets a day
    ~694     tweets an hour
    ~11      tweets a minute
    """
    while (True):
        data = self.search(MAX_RESULTS=11)
        if (data != None):
            self.append_data(data)
        time.sleep(60)
    
  def addSentiment(self):
    """
    You only need to run this once, the csv file is overwritten with the sentiment now added
    """
    df = pd.read_csv(self.csv_file, error_bad_lines=False)
    analyzer = SentimentIntensityAnalyzer()
    length = len(df.index)
    sentiments = []

    widgets = [
        '\x1b[ Analyzing Sentiment\x1b[39m',
        progressbar.Percentage(),
        progressbar.Bar(marker='\x1b[32m#\x1b[39m'),
    ]
    bar = progressbar.ProgressBar(widgets=widgets, max_value=length).start()

    for index, row in df.iterrows():
      sentiment = analyzer.polarity_scores(row["text"])['compound']
      sentiments.append(sentiment)
      bar.update(index)
    bar.finish()
    df['sentiment'] = sentiments
    df.to_csv(self.csv_file)
  
  def toDataPoints(self, timeframe=30):
    """
    You only need to run this once, the data points are saved to a new csv matching the format "[out_path]_[timeframe]min"
    """
    df = pd.read_csv(self.csv_file, error_bad_lines=False)
    origin = pd.to_datetime(df['created_at'][0])
    datapoints = []
    current_data_point = DataPoint(origin)

    widgets = [
        '\x1b[ Converting to Datapoints\x1b[39m',
        progressbar.Percentage(),
        progressbar.Bar(marker='\x1b[32m#\x1b[39m'),
    ]
    bar = progressbar.ProgressBar(widgets=widgets, max_value=len(df.index)).start()
    bar.update(0)
    
    for index, row in df.iterrows():
      current_time = pd.to_datetime(row['created_at'], errors='coerce')
      if (current_time - origin).total_seconds() > (timeframe * 60): # keep time frame consistently in minutes
        origin = current_time
        datapoints.append(current_data_point)
        current_data_point = DataPoint(current_time)
      current_data_point.add_entry(row['sentiment'])
      bar.update(index)
    bar.finish()
    temp = pd.DataFrame([x.as_dict() for x in datapoints])
    temp.to_csv(self.csv_file + "_{}min.csv".format(timeframe))
    return datapoints