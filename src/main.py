import pandas as pd
import seaborn as sn
import matplotlib.pyplot as plt
from scipy.stats import spearmanr

import config
from utilities.historical_data import TwitterHistorical
from utilities.stream_data import TwitterStream
from models.linear_regression import LR
from models.neural_network import MLP

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
#
# Merge data points and price data by closest date within a timeframe
# TwitterHistorical.merge_with_historical(data_points, price_data, timeframe=1440, offset=1440)

# STREAMING
# x = TwitterStream(config.bearer_token)
#
# Start streaming tweets
# x.start()

# ANALYZE MODEL CORRELATIONS
def show_correlation_matrix(dataframe, method='kendall'):
  matrix = dataframe.corr(method=method)
  sn.heatmap(matrix, annot=True)
  plt.show()

# Models
df = pd.read_csv("/home/jack/Desktop/mqp/twitter_data_collector/data/price_and_sentiment.csv")
df = df.dropna()
df = df.drop(['High', 'Low', 'Close', 'Daily Net', 'Date'], axis=1)

show_correlation_matrix(df)
k = MLP(df.drop(['Percent Gained'], axis=1), df['Percent Gained'])
k.test()
k.evaluate()



