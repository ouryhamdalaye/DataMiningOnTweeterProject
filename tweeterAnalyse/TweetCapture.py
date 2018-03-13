from tweeterAnalyse import *

class TweetCapture(object):
    def __init__(self):
        ''
    def getTweetsFromQuery(self, pApi, pQuery, pMaxTweets):
        return [status for status in tweepy.Cursor(pApi.search, q=pQuery).items(pMaxTweets)]

# documents= public_tweets
#
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