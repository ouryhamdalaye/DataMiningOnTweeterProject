from tweeterAnalyse import *
import time
import tweepy


class DataCapture(object):

    @staticmethod
    def get_tweets_from_query(api, query, max_tweets):
        statuses_json = []
        count = 0
        for status in tweepy.Cursor(api.search, q=query, tweet_mode='extended', lang=LANG_ISO639_1).items(max_tweets) :
            statuses_json.append(status._json)
            time.sleep(70)
            count += 1
            print(round(count * 100.0 / max_tweets, 1))
        return statuses_json