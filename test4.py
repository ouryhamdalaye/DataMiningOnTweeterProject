import pandas as pd
import nltk
from nltk.stem.porter import PorterStemmer
from nltk.corpus import wordnet as wn
import itertools


"""
exemple :
sent1 = "I love riding bike"
sent2 = "I enjoy riding bikes"
"""
def get_similarity_between_two_tweets(tweet1, tweet2):

    # use stemmer
    stm = PorterStemmer()
    # Convert the tag given by nltk.pos_tag to the tag used by wordnet.synsets
    tag_dict = {'N': 'n', 'J': 'a', 'R': 'r', 'V': 'v'}

    s1 = nltk.pos_tag(nltk.word_tokenize(tweet1))

    s1 = dict(filter(lambda x: len(x[1])>0,
                     map(lambda row: (row[0],wn.synsets(
                           stm.stem(row[0]),
                           tag_dict[row[1][0]])) if row[1][0] in tag_dict.keys()
                         else (row[0],[]),s1)))

    s2 = nltk.pos_tag(nltk.word_tokenize(tweet2))

    s2 = dict(filter(lambda x: len(x[1])>0,
                     map(lambda row: (row[0],wn.synsets(
                              stm.stem(row[0]),
                              tag_dict[row[1][0]])) if row[1][0] in tag_dict.keys()
                         else (row[0],[]),s2)))

    res = {}
    for w2,gr2 in s2.items():
        for w1,gr1 in s1.items():
            tmp = pd.Series(list(map(lambda row: row[1].path_similarity(row[0]),
                                     itertools.product(gr1,gr2)))).dropna()
            if len(tmp)>0:
                res[(w1,w2)] = tmp.max()
    print(res)

    similarity = pd.Series(res).groupby(level=0).max().mean()
    print(similarity)

""" install all necessary packages for nltk """
    @staticmethod
    def init():
        # install punkt
        nltk.download('punkt')
        # install stopwords
        nltk.download('stopwords')
        # install averaged_perceptron_tagger
        nltk.download('averaged_perceptron_tagger')
        # install wordnet
        nltk.download('wordnet')

    """ tokenize tweets text by words """
    @staticmethod
    def tokenize_tweet_by_words(tweet_text):
        words = word_tokenize(tweet_text)
        return words

    """ tokenize tweets text by sentences """
    @staticmethod
    def tokenize_tweet_by_sentences(tweet_text):
        custom_sent_tokenizer = PunktSentenceTokenizer()
        return custom_sent_tokenizer.tokenize(tweet_text)

    """ remove stop words """
    @staticmethod
    def remove_stop_words(tweet_word_tokenized):
        stop_words = set(stopwords.words(LANG))
        return [w for w in tweet_word_tokenized if not w in stop_words]

    """ stem words """
    @staticmethod
    def stem_words(tweet_without_stop_words):
        ps = PorterStemmer()
        filtered_words = []
        for w in tweet_without_stop_words:
            filtered_words.append(ps.stem(w))
        return filtered_words

    """ Part of speech tagging :  labeling words in a sentence as nouns, adjectives, verbs...etc' """
    @staticmethod
    def speech_tag(tweet_stemmed):
        tagged = []
        try:
            tagged = nltk.pos_tag(tweet_stemmed)
        except Exception as e:
            print(str(e))
        return tagged

    """ chunk words """
    @staticmethod
    def chunk(speech_tag):
        chunk_gram = r"""Chunk: {<RB.?>*<VB.?>*<NNP>+<NN>?}"""
        chunk_parser = nltk.RegexpParser(chunk_gram)
        chunked = chunk_parser.parse(speech_tag)

        print(chunked)
        for subtree in chunked.subtrees(filter=lambda t: t.label() == 'Chunk'):
            print(subtree)

        chunked.draw()

"""
                    tweet_text = ""
                    try:
                        tmp = i['retweeted_status']
                        tweet_text = i['retweeted_status']['full_text']
                        print("b " + tweet_text)
                    except Exception:
                        tweet_text = i['full_text']
                        print("a " + tweet_text)

                    print("\n\nData Pre-Treatment --\n")

                    print("\n--- Init nltk ---\n")
                    DataPreTreatment.init()

                    print("\n----------\n")

                    print("\nsentence tokenize")
                    tweet_sentence_tokenized = DataPreTreatment.tokenize_tweet_by_sentences(tweet_text)
                    print(tweet_sentence_tokenized)
                    print("\n")

                    print("\nword tokenize")
                    tweet_word_tokenized = DataPreTreatment.tokenize_tweet_by_words(tweet_text)
                    print(tweet_word_tokenized)
                    print("\n")

                    print("\nremove stopwords")
                    tweet_without_stop_words = DataPreTreatment.remove_stop_words(tweet_word_tokenized)
                    print(tweet_without_stop_words)
                    print("\n")

                    print("\nstem")
                    tweet_stemmed = DataPreTreatment.stem_words(tweet_without_stop_words)
                    print(tweet_stemmed)
                    print("\n")

                    print("\nspeech tag")
                    speech_tag = DataPreTreatment.speech_tag(tweet_stemmed)
                    print(speech_tag)
                    print("\n")
                    """