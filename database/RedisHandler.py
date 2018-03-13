from database import *

class RedisHandler(object):
    def __init__(self):
        self.r = redis.StrictRedis(host=REDIS_HOST_ADDRESS, port=REDIS_PORT, db=REDIS_DB)

    def saveTweetsToRedis(self, pTweets, pRedisTweetTag):
        self.r.set(pRedisTweetTag, pTweets)

    def retrieveTweets(self, pRedisTweetTag):
        return self.r.get(pRedisTweetTag)