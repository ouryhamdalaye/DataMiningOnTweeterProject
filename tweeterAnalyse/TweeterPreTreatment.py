from tweeterAnalyse import *
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer

class TweetPreTreatment(object):
    def __init__(self, sn = [], text = [], timestamp = [],):
        self.sn = sn
        self.text = text
        self.timestamp = timestamp

    'pTimeStamp = tweet.created_at, pSn = tweet.user.screen_name, pText = tweet.text'
    def convertTweetsListToDataframe(self):
        df = pd.DataFrame()
        df['sn'] = self.sn
        df['text'] = self.text
        df['timestamp'] = self.timestamp
        return df

    'tokenise tweets text'
    def tokeniseTweets(self, pTweetText):
        words = word_tokenize(pTweetText)
        return words

    'remove step words'
    def removeStopWords(self, words):
        stop_words = set(stopwords.words("french"))
        return [w for w in words if not w in stop_words]

    'retrieve stem words '
    def stemWords(self, words):
        ps = PorterStemmer()
        filtered_words = []
        for w in words:
            filtered_words.append(ps.stem(w))
        return filtered_words


