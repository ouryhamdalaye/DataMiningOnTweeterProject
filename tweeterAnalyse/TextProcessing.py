from tweeterAnalyse import *
from nltk.corpus import stopwords, state_union
from nltk.tokenize import word_tokenize, PunktSentenceTokenizer
from nltk.stem.porter import PorterStemmer
from nltk.corpus import wordnet as wn
import itertools

class TextProcessing(object):

    def __init__(self):
        """"""
        # install punkt
        # nltk.download('punkt')
        # install stopwords
        # nltk.download('stopwords')
        # install averaged_perceptron_tagger
        # nltk.download('averaged_perceptron_tagger')
        # install wordnet
        # nltk.download('wordnet')

    def get_similarity_between_two_tweets(self, tweet1, tweet2):
        # use stemmer
        stm = PorterStemmer()
        # Convert the tag given by nltk.pos_tag to the tag used by wordnet.synsets
        tag_dict = {'N': 'n', 'J': 'a', 'R': 'r', 'V': 'v'}

        s1 = nltk.pos_tag(nltk.word_tokenize(tweet1))

        s1 = dict(filter(lambda x: len(x[1]) > 0,
                         map(lambda row: (row[0], wn.synsets(
                             stm.stem(row[0]),
                             tag_dict[row[1][0]])) if row[1][0] in tag_dict.keys()
                         else (row[0], []), s1)))

        s2 = nltk.pos_tag(nltk.word_tokenize(tweet2))

        s2 = dict(filter(lambda x: len(x[1]) > 0,
                         map(lambda row: (row[0], wn.synsets(
                             stm.stem(row[0]),
                             tag_dict[row[1][0]])) if row[1][0] in tag_dict.keys()
                         else (row[0], []), s2)))

        res = {}
        for w2, gr2 in s2.items():
            for w1, gr1 in s1.items():
                tmp = pd.Series(list(map(lambda row: row[1].path_similarity(row[0]),
                                         itertools.product(gr1, gr2)))).dropna()
                if len(tmp) > 0:
                    res[(w1, w2)] = tmp.max()
        # print(res)

        similarity = pd.Series(res).groupby(level=0).max().mean()
        # print(similarity)
        return similarity

    """
    build a dict like 'user_id : tweet_text'
    """
    @staticmethod
    def get_tweet_textes_with_users(tweet_texts, tweet_json):

        current_tweet_text = TextProcessing.get_tweet_text(tweet_json)

        # check if one text was already saved, otherwise you have nothing to compare
        if (len(tweet_texts) == 0):
            tweet_texts[tweet_json['user']['id_str']] = [current_tweet_text]
        else:
            try:
                tweet_texts[tweet_json['user']['id_str']].append(current_tweet_text)
            except KeyError:
                tweet_texts[tweet_json['user']['id_str']] = [current_tweet_text]
        return tweet_texts

    @staticmethod
    def get_tweet_text(tweet_json):
        tweet_text = ""
        # get tweet text
        try:
            tweet_text = tweet_json['retweeted_status']['full_text']
        except Exception:
            tweet_text = tweet_json['full_text']
        finally:
            return tweet_text