from database import *


class RedisHandler(object):
    def __init__(self):
        self.r = redis.StrictRedis(host=REDIS_HOST_ADDRESS, port=REDIS_PORT, db=REDIS_DB)

    def save_tweets_to_redis(self, tweets, redis_tweet_tag):
        self.r.set(redis_tweet_tag, tweets)

    def retrieve_tweets(self, redis_tweet_tag):
        return self.r.get(redis_tweet_tag).decode('utf-8')