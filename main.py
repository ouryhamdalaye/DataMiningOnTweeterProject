from constants.constants import *
from database.RedisHandler import RedisHandler
from config.Authentification import Authentification
from tweeterAnalyse.TweetCapture import TweetCapture
from tweeterAnalyse.TweeterPreTreatment import TweetPreTreatment
import json

auth = Authentification()
tweeterCapture = TweetCapture()
tweeterPreTreatment = TweetPreTreatment()
redisHandler = RedisHandler()

# authentificate to tweeter
api = auth.auth(pConsumerKey=CONSUMER_KEY, pConsumerSecret=CONSUMER_SECRET, pAccessToken=ACCESS_TOKEN, pAccessTokenSecret=ACCESS_TOKEN_SECRET)

# get tweets
query = 'real and psg'
maxTweets = 1
searchTweets = tweeterCapture.getTweetsFromQuery(api, query, maxTweets)
# # print results
for tweet in searchTweets:
     print(tweet.text)

# save tweets to Redis
redisTweetsTag = "realpsgtweets"
redisTimestampTag = "realpsgtweetsTimestamp"
redisSnTag = "realpsgtweetsSn"

#      #print(tweet.user.screen_name, tweet.created_at, tweet.text)
#      tweeterPreTreatment.timestamp.append(tweet.created_at)
#      tweeterPreTreatment.sn.append(tweet.user.screen_name)
#      tweeterPreTreatment.text.append(tweet.text)

#print(tweet)


redisHandler.saveTweetsToRedis(pTweets=searchTweets, pRedisTweetTag=redisTweetsTag)
#redisHandler.saveTweetsToRedis(pTweets=tweeterPreTreatment.sn, pRedisTweetTag=redisSnTag)
#redisHandler.saveTweetsToRedis(pTweets=tweeterPreTreatment.timestamp, pRedisTweetTag=redisTimestampTag)

tweets = redisHandler.retrieveTweets(pRedisTweetTag=redisTweetsTag)
#tweetsTimeStamp = redisHandler.retrieveTweets(pRedisTweetTag=redisTextTag)
#tweetsSn = redisHandler.retrieveTweets(pRedisTweetTag=redisTextTag)



#print(test)

# Create lists for each field desired from the tweets.
# for tweet in searchTweets:
#     print(tweet.user.screen_name, tweet.created_at, tweet.text)
#     tweeterPreTreatment.timestamp.append(tweet.created_at)
#     tweeterPreTreatment.sn.append(tweet.user.screen_name)
#     tweeterPreTreatment.text.append(tweet.text)
#
# tweeterPreTreatment.convertTweetsListToDataframe()


#preTreatment