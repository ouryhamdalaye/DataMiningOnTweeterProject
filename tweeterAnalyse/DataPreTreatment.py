from tweeterAnalyse import *
from tweeterAnalyse.TextProcessing import TextProcessing


class DataPreTreatment(object):

    voc_df = pd.DataFrame(columns=['userFromId', 'userToId'])
    tweet_texts = {}

    @staticmethod
    def build_hashtags_dict(tweet_json):
        hashtag_dict = {}
        try:
            for hashtag in tweet_json['entities']['hashtags']:
                try:
                    hashtag_dict[hashtag['text']].append(tweet_json['user']['id_str'])
                except KeyError:
                    hashtag_dict[hashtag['text']] = [tweet_json['user']['id_str']]
            # print(DataPreTreatment.hashtag_dict)
        except Exception as e:
            print("")
        finally:
            return hashtag_dict

    @staticmethod
    def build_urls_dict(tweet_json):
        urls_dict = {}
        try:
            for url in tweet_json['entities']['urls']:
                try:
                    urls_dict[url['url']].append(tweet_json['user']['id_str'])
                except KeyError:
                    urls_dict[url['url']] = [tweet_json['user']['id_str']]
            # print(DataPreTreatment.urls_dict)
        except Exception as e:
            print("")
        finally:
            return urls_dict

    @staticmethod
    def build_voc_dict(tweet_json, tweet_texts):
        frames = []
        df_voc = pd.DataFrame(columns=['userFromId', 'userToId'])
        current_tweet_text = TextProcessing.get_tweet_text(tweet_json)
        try:
            tp = TextProcessing()
            for user_id, texts in tweet_texts.items():
                for text in texts:
                    df_tmp = pd.DataFrame(columns=['userFromId', 'userToId'])
                    if not user_id == tweet_json['user']['id_str']:
                        if(tp.get_similarity_between_two_tweets(current_tweet_text, text) > 0.7):
                            df_tmp['userFromId'] = pd.Series([tweet_json['user']['id_str']])
                            df_tmp['userToId'] = pd.Series([user_id])
                            frames.append(df_tmp)
            df_voc = pd.concat(frames)
            # print(DataPreTreatment.frames)
        except Exception as e:
            print("")
        finally:
            return df_voc

