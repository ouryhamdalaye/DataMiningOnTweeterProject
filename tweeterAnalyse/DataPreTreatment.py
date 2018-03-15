from tweeterAnalyse import *
from nltk.corpus import stopwords, state_union
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize, PunktSentenceTokenizer


class DataPreTreatment(object):

    """ install all necessary packages for nltk """
    @staticmethod
    def init():
        # install punkt
        nltk.download('punkt')
        # install stopwords
        nltk.download('stopwords')
        # install averaged_perceptron_tagger
        nltk.download('averaged_perceptron_tagger')

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
