import pandas as pd
import config
from utilities.historical_data import TwitterHistorical
from utilities.stream_data import TwitterStream
from models.linear_regression import KNN

# HISTORICAL
x = TwitterHistorical(config.consumer_key, config.secret_consumer_key, config.access_key, config.secret_access_key, "C:/Users/Jack/Desktop/Twitter-data-collector/data/tweets.csv")
# 
# Start collecting tweets, export them to the path specified
# x.start()
# 
# Add compound sentiment score to the collected tweets
# x.addSentiment()
#
# Average sentiment, tweet occurances, timestarted, and variance within timeframe
# x.toDataPoints(timeframe=(30))

# STREAMING
# x = TwitterStream(config.bearer_token)
#
# Start streaming tweets
# x.start()

# sentiment_data = pd.read_csv("data/tweets.csv_1440min.csv")
# price_data = pd.read_csv("data/ETH-USD.csv")
# df = price_data.join(sentiment_data, rsuffix='r')
# df = df.dropna()
# labels = df["Close"]
# data = df.drop(['Close', 'Adj Close', 'Date', 'date', 'Unnamed: 0'], axis=1)
# model = KNN(data, labels)
# model.train()
# model.test()
