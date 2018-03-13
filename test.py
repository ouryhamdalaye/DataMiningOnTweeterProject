import tweepy
import redis

# The user credential variables to access Twitter API
access_token = "243510610-uW7TEaqISBwB86VCfQh0gczU6WaTwIX4xr2CHvt3"
access_token_secret = "lGmSgFPFzAPFLQ2THFqEG7OUg8akd5WusbijZuh9UlqHl"
consumer_key = "QtM1L0ppK6KPC2OXaAqRHwsrP"
consumer_secret = "1AYVWMuePpHWRGgR2AIiuM9fGp0bAVoGF4mmPUiqXoIpnDRHwh"

# Authentication

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

query = 'savoie'
max_tweets = 10

public_tweets = [status for status in tweepy.Cursor(api.search, q=query).items(max_tweets)]

# Results
for tweet in public_tweets:
    print(tweet.text)

r = redis.StrictRedis(host='localhost', port=6379, db=0)
r.set('tweet', public_tweets)