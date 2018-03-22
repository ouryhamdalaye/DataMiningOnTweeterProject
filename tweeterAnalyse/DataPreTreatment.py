from tweeterAnalyse import *
from tweeterAnalyse.TextProcessing import TextProcessing


class DataPreTreatment(object):

    hashtag_dict = {}
    urls_dict = {}
    voc_df = pd.DataFrame()
    tweet_texts = {}

    @staticmethod
    def build_hashtags_dict(tweet_json):
        try:
            for hashtag in tweet_json['entities']['hashtags']:
                try:
                    DataPreTreatment.hashtag_dict[hashtag['text']].append(tweet_json['user']['id_str'])
                except KeyError:
                    DataPreTreatment.hashtag_dict[hashtag['text']] = [tweet_json['user']['id_str']]
            print(DataPreTreatment.hashtag_dict)
        except Exception as e:
            print("")

    @staticmethod
    def build_urls_dict(tweet_json):
        try:
            for url in tweet_json['entities']['urls']:
                try:
                    DataPreTreatment.urls_dict[url['url']].append(tweet_json['user']['id_str'])
                except KeyError:
                    DataPreTreatment.urls_dict[url['url']] = [tweet_json['user']['id_str']]
            print(DataPreTreatment.urls_dict)
        except Exception as e:
            print("")

    @staticmethod
    def build_voc_dict(tweet_json):
        try:
            # get tweet text
            try:
                tweet_text = tweet_json['retweeted_status']['full_text']
            except Exception:
                tweet_text = tweet_json['full_text']

            # check if one text was already saved, otherwise you have nothing to compare
            if(len(DataPreTreatment.tweet_texts) == 0):
                DataPreTreatment.tweet_texts[tweet_json['user']['id_str']] = [tweet_text]
            else:
                try:
                    DataPreTreatment.tweet_texts[tweet_json['user']['id_str']].append(tweet_text)
                except KeyError:
                    DataPreTreatment.tweet_texts[tweet_json['user']['id_str']] = [tweet_text]

                tp = TextProcessing()
                for user_id, texts in DataPreTreatment.tweet_texts.items():
                    for text in texts:
                        similarity = tp.get_similarity_between_two_tweets(tweet_text, text)
                        if(similarity > 0.6):
                            DataPreTreatment.voc_df['userFromId'] = pd.Series([tweet_json['user']['id_str']])
                            DataPreTreatment.voc_df['userToId'] = pd.Series([user_id])

            print(DataPreTreatment.voc_dict)
        except Exception as e:
            print("")

