# Tweeter Authentication Class
from config import *

class Authentification(object):

    def auth(self, pConsumerKey, pConsumerSecret, pAccessToken, pAccessTokenSecret):
        auth = tweepy.OAuthHandler( pConsumerKey, pConsumerSecret)
        auth.set_access_token(pAccessToken, pAccessTokenSecret)
        api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
        return api