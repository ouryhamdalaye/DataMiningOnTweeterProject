from tweeterAnalyse import *


class DataDirectLinkHelper(object):

    @staticmethod
    def get_direct_links(tweet):
        df_direct_link = pd.DataFrame(columns=['userFromId','userToId'])
        df_direct_link1 = DataDirectLinkHelper.connect_user_by_retweet(tweet)
        df_direct_link2 = DataDirectLinkHelper.connect_user_by_reply(tweet)
        df_direct_link3 = DataDirectLinkHelper.connect_user_by_mention(tweet)
        frames = []
        if not df_direct_link1.empty:
            frames.append(df_direct_link1)
        if not df_direct_link2.empty:
            frames.append(df_direct_link2)
        if not df_direct_link3.empty:
            frames.append(df_direct_link3)
        if not len(frames) == 0:
            return pd.concat(frames)
        return df_direct_link

    @staticmethod
    def connect_user_by_retweet(tweet_json):
        df_connect = pd.DataFrame()
        try:
            if tweet_json['retweeted_status']:
                df_connect['userFromId'] = pd.Series([tweet_json['user']['id_str']])
                df_connect['userToId'] = pd.Series([tweet_json['retweeted_status']['user']['id_str']])
        except Exception as e:
            print("")
            # print("Warning at connect_user_by_retweet : no " + str(e))
        finally:
            return df_connect


    @staticmethod
    def connect_user_by_reply(tweet_json):
        df_connect = pd.DataFrame()
        try:
            if tweet_json['in_reply_to_user_id_str']:
                df_connect['userFromId'] = pd.Series([tweet_json['user']['id_str']])
                df_connect['userToId'] = pd.Series([tweet_json['in_reply_to_user_id_str']])
        except Exception as e:
            print("")
            # print("Warning at connect_user_by_reply : " + str(e))
        finally:
            return df_connect


    @staticmethod
    def connect_user_by_mention(tweet_json):
        df_connect = pd.DataFrame()
        try:
            if tweet_json['entities']['user_mentions']:
                for user_mention in tweet_json['entities']['user_mentions']:
                    df_connect['userFromId'] = pd.Series([tweet_json['user']['id_str']])
                    df_connect['userToId'] = pd.Series([user_mention['id_str']])
        except Exception as e:
            print("")
            # print("Warning at connect_user_by_mention : " + str(e))
        finally:
            return df_connect

