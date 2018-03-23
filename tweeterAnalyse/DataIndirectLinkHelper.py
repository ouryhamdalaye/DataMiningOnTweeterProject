from tweeterAnalyse import *


class DataIndirectLinkHelper(object):

    @staticmethod
    def get_indirect_links(hashtags, urls, vocabularies):
        df_indirect_link1 = DataIndirectLinkHelper.get_connected_users_by_hashtags_as_data_frame(hashtag_table_dict = hashtags)
        df_indirect_link2 = DataIndirectLinkHelper.get_connected_users_by_urls_as_data_frame(urls_table_dict = urls)
        df_indirect_link3 = DataIndirectLinkHelper.get_connected_users_by_vocabulary(vocabularies = vocabularies)
        frames = []
        if not df_indirect_link1.empty :
            frames.append(df_indirect_link1)
        if not df_indirect_link2.empty :
            frames.append(df_indirect_link2)
        if not df_indirect_link3.empty :
            frames.append(df_indirect_link3)
        return frames

    @staticmethod
    def _create_user_ids_connections_from_dict(users_ids, df_connect = None):
        if df_connect.empty:
            df_connect = pd.DataFrame(columns=['userFromId', 'userToId'])
        try:
            frames = []
            df_tmp = pd.DataFrame(columns=['userFromId', 'userToId'])
            current_user_id = users_ids.pop(0)
            for user_id in users_ids:
                df_tmp['userFromId'] = [current_user_id]
                df_tmp['userToId'] = [user_id]
                frames.append(df_tmp)
            if not len(frames) == 0:
                df_connect = pd.concat(frames)
            if len(users_ids) > 1:
                DataIndirectLinkHelper._create_user_ids_connections_from_dict(users_ids, df_connect)
        except KeyError as k:
            print(str(k))
        finally:
            return df_connect

    """ build a dataframe with hash_tags connections between users
        hashtag_table : dictionnary like: {"hashtag1": [user1, user2], "hashtag2": [], "hashtag3": []}:
    """
    @staticmethod
    def get_connected_users_by_hashtags_as_data_frame(hashtag_table_dict):
        df_connected_hashtags = pd.DataFrame(columns=['userFromId', 'userToId'])
        frames = []
        for hahstag, user_ids in hashtag_table_dict.items():
            if len(user_ids) > 1:
                frames.append(DataIndirectLinkHelper._create_user_ids_connections_from_dict(user_ids, df_connected_hashtags))
        if not len(frames) == 0:
            df_connected_hashtags = pd.concat(frames)
        return df_connected_hashtags

    """ build a dataframe with urls connections between users
            urls_table : dictionnary like: {"url1": [user1, user2], "hashtag2": [], "hashtag3": []}:
    """
    @staticmethod
    def get_connected_users_by_urls_as_data_frame(urls_table_dict):
        df_connected_urls = pd.DataFrame(columns=['userFromId', 'userToId'])
        frames = []
        for url, user_ids in urls_table_dict.items():
            if len(user_ids) > 1:
                frames.append(DataIndirectLinkHelper._create_user_ids_connections_from_dict(user_ids, df_connected_urls))
        if not len(frames) == 0:
            df_connected_urls = pd.concat(frames)
        return df_connected_urls

    """ build a dataframe with vocabulary connections between users
            voc_table : dictionnary like: {"vocabulary1": [user1, user2], "vocabulary1": [], "hashtag3": []}:
    """
    @staticmethod
    def get_connected_users_by_vocabulary(vocabularies):
        voc_frames_not_emty = []
        for voc in vocabularies:
            if not voc.empty:
                voc_frames_not_emty.append(voc)

        df = pd.DataFrame(columns=['userFromId', 'userToId'])
        try:
            df = pd.concat(vocabularies)
        except Exception as e:
            print(str(e) + "could not create vocabularies connections")
        return df


