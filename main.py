from historicalData import TwitterHistorical
from streamData import TwitterStream

import config

# HISTORICAL
# x = TwitterHistorical(config.consumer_key, config.secret_consumer_key, config.access_key, config.secret_access_key, config.data_path)
# 
# Start collecting tweets, export them to a path
# x.start()
# 
# Add compound sentiment score to the collected tweets
# x.addSentiment()
#
# Average sentiment and tweet frequency within timeframe
# x.toDataPoints()

# STREAMING
# x = TwitterStream(config.bearer_token)
#
# Start streaming tweets
# x.start()

x = TwitterHistorical(config.consumer_key, config.secret_consumer_key, config.access_key, config.secret_access_key, config.data_path)
x.toDataPoints()
