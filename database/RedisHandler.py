from database import *
import pandas as pd


class RedisHandler(object):
    def __init__(self):
        self.r = redis.StrictRedis(host=REDIS_HOST_ADDRESS, port=REDIS_PORT, db=REDIS_DB)

    def save_tweets_to_redis(self, tweets, redis_tweet_tag):
        self.r.set(redis_tweet_tag, tweets)

    def retrieve_tweets(self, redis_tweet_tag):
        return self.r.get(redis_tweet_tag).decode('utf-8')

    def save_dataframe_to_redis(self, dataframe, redis_df_tag):
        self.r.set(redis_df_tag, dataframe.to_msgpack(compress='zlib'))

    def retrieve_dataframe(self, redis_df_tag):
        return pd.read_msgpack(self.r.get(redis_df_tag))
