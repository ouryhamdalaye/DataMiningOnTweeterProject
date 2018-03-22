from tweeterAnalyse import *
from tweeterAnalyse.DataPreTreatment import DataPreTreatment


class DataIndirectLinkHelper(object):

    @staticmethod
    def get_indirect_links(tweet):
        df_direct_link1 = DataIndirectLinkHelper.get_connected_users_by_hashtags_as_data_frame(DataPreTreatment.hashtag_dict)
        #DataPreTreatment.get_urls_dict()
        df_direct_link2 = DataIndirectLinkHelper.get_connected_users_by_urls_as_data_frame(tweet)
        #DataPreTreatment.get_voc_dict()
        df_direct_link3 = DataIndirectLinkHelper.get_connected_users_by_vocabulary(tweet)
        frames = [df_direct_link1, df_direct_link2, df_direct_link3]
        return pd.concat(frames)


    @staticmethod
    def _create_user_ids_connections_for_data_frames(users_ids = [], df_connect = None):
        if df_connect == None:
            df_connect = pd.DataFrame()
        try:
            current_user_id = users_ids.pop(0)
            for user_id in users_ids:
                df_connect['userFromId'] = pd.Series([current_user_id])
                df_connect['userToId'] = pd.Series([user_id])

            if not len(users_ids) == 0:
                DataIndirectLinkHelper._create_user_ids_connections_for_data_frames(users_ids, df_connect)
        except KeyError as k:
            print(str(k))
        finally:
            return df_connect

    """ build a dataframe with hash_tags connections between users
        hashtag_table : dictionnary like: {"hashtag1": [user1, user2], "hashtag2": [], "hashtag3": []}:
    """
    @staticmethod
    def get_connected_users_by_hashtags_as_data_frame(hashtag_table_dict):
        df_connected_hashtags = pd.DataFrame()
        for hahstag, user_ids in hashtag_table_dict.items():
            df_connected_hashtags = pd.concat(DataIndirectLinkHelper._create_user_ids_connections_for_data_frames(user_ids, df_connected_hashtags))
        return df_connected_hashtags

    """ build a dataframe with urls connections between users
            urls_table : dictionnary like: {"url1": [user1, user2], "hashtag2": [], "hashtag3": []}:
    """
    @staticmethod
    def get_connected_users_by_urls_as_data_frame(urls_table_dict):
        df_connected_urls = pd.DataFrame()
        for url, user_ids in urls_table_dict.items():
            df_connected_urls = pd.concat(DataIndirectLinkHelper._create_user_ids_connections_for_data_frames(user_ids, df_connected_urls))
        return df_connected_urls

    """ build a dataframe with vocabulary connections between users
            voc_table : dictionnary like: {"vocabulary1": [user1, user2], "vocabulary1": [], "hashtag3": []}:
    """
    @staticmethod
    def get_connected_users_by_vocabulary(voc_table):
        voc_concordances = pd.DataFrame()
        for url, user_ids in voc_table.items():
            voc_concordances = pd.concat(DataIndirectLinkHelper._create_user_ids_connections_for_data_frames(user_ids, voc_concordances))
        return voc_concordances


