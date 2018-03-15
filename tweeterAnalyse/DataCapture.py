from tweeterAnalyse import *
import time


class DataCapture(object):

    @staticmethod
    def get_tweets_from_query(api, query, max_tweets):
        statuses_json = []
        count = 0
        for status in tweepy.Cursor(api.search, q=query, tweet_mode='extended', lang=LANG_ISO639_1).items(max_tweets) :
            statuses_json.append(status._json)
            #time.sleep(70)
            count += 1
            print(round(count * 100.0 / max_tweets, 1))
        return statuses_json

# documents= public_tweets
# lang=language, count=tweetCount, tweet_mode='extended')
# random.shuffle(documents)
#
# all_words =[]
#
# for w in public_tweets:
#     #print(w.text)
#     #print("======================================")
#     all_words.append(w.text)
#
# all_words = nltk.FreqDist(all_words)
#
# word_features = list(all_words.keys())[:300]
#
# print(word_features)