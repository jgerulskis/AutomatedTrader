import pandas as pd
import config
from utilities.historical_data import TwitterHistorical
from utilities.stream_data import TwitterStream
from models.linear_regression import KNN

# HISTORICAL
# x = TwitterHistorical(config.consumer_key, config.secret_consumer_key, config.access_key, config.secret_access_key, "/home/jack/Desktop/mqp/twitter_data_collector/data/tweets.csv")
# 
# Start collecting tweets, export them to the path specified
# x.start()
# 
# Add compound sentiment score to the collected tweets
# x.add_sentiment()
#
# Average sentiment, tweet occurances, timestarted, and variance within timeframe
# x.to_data_points(timeframe=1)

# STREAMING
# x = TwitterStream(config.bearer_token)
#
# Start streaming tweets
# x.start()

data_points = pd.read_csv("/home/jack/Desktop/mqp/twitter_data_collector/data/tweets.csv_1min.csv")
price_data = pd.read_csv("/home/jack/Desktop/mqp/twitter_data_collector/data/ETHUSD1min.csv")
TwitterHistorical.merge_with_historical(data_points, price_data, timeframe=1)


