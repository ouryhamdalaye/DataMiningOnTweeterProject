from constants.Constants import *
from database.RedisHandler import RedisHandler
from config.Authentication import Authentication
from tweeterAnalyse.DataCapture import DataCapture
from tweeterAnalyse.DataPreTreatment import DataPreTreatment
from tweeterAnalyse.DataDirectLinkHelper import DataDirectLinkHelper
from tweeterAnalyse.DataIndirectLinkHelper import DataIndirectLinkHelper
from tweeterAnalyse.TextProcessing import TextProcessing
from tweeterAnalyse.GraphDrawer import GraphDrawer
import matplotlib.pyplot as plt

import json as json
import pandas as pd
import sys

# authenticate to tweeter
api = Authentication.auth(consumer_key=CONSUMER_KEY, consumer_secret=CONSUMER_SECRET, access_token=ACCESS_TOKEN,
                access_token_secret=ACCESS_TOKEN_SECRET)

redis_handler = RedisHandler()
ans = True
redis_tweet_tag = ""
query = 'sarkozy'
while ans:
    print("""
    1.Look for a subject (Default : "espion")
    2.Analyse subject
    3.Visualize subject
    q.Exit/Quit
    """)
    ans = input("What would you like to do? ")
    # ans = "2"
    if ans == "1":
        print("\nLook for a subject ")
        # get tweets
        max_tweets = 4000
        query_bis = input("Type a subject : (Press Enter for Default) ")
        if query_bis == "":
            print("Looking for default subject : " + query)
            query_bis = query
        else:
            query = query_bis
        print("\nThis may take a while...")
        search_tweets = DataCapture.get_tweets_from_query(api=api, query=query_bis, max_tweets=max_tweets)
        json_tweets = json.dumps(search_tweets)

        # save tweets to Redis
        redis_tweet_tag = "tweets_query_" + query_bis
        redis_handler.save_tweets_to_redis(tweets=json_tweets, redis_tweet_tag=redis_tweet_tag)
    elif ans == "2":
        if redis_tweet_tag == "":
            print("Default subject : " + query )
            redis_tweet_tag = "tweets_query_" + query
        print("\nAnalyse of subject " + query)
        try:
            tweets = json.loads(redis_handler.retrieve_tweets(redis_tweet_tag=redis_tweet_tag))
            if not tweets:
                print("\nUnable to load payload. Please Look for a subject again.")
            else:
                hashtags_dict = {}
                urls_dict = {}
                tweet_texts = {}

                voc_frames = []
                direct_links_frames = []

                df_direct_links = pd.DataFrame()
                df_indirect_links = pd.DataFrame(columns=['userFromId', 'userToId'])

                count = 0
                nbTweets = len(tweets)

                # pre-treatment
                print("pre-treatment")
                for tweet in tweets:
                    tweet_texts.update(TextProcessing.get_tweet_textes_with_users(tweet_texts, tweet))
                    hashtags_dict.update(DataPreTreatment.build_hashtags_dict(tweet))
                    urls_dict.update(DataPreTreatment.build_urls_dict(tweet))

                    count += 1
                    per = round(count * 100.0 / nbTweets, 1)
                    sys.stdout.write("\rbuilding direct links. %s%% completed" % per)
                    sys.stdout.flush()
                    # direct links can directly be built in this loop
                    direct_links_frames.append(DataDirectLinkHelper.get_direct_links(tweet))

                print("\npre-treatment done")
                print("\n---------------\n")

                exit(0)

                DataPreTreatment.build_voc_dict(tweet, tweet_texts)
                voc_frames.append(DataPreTreatment.build_voc_dict(tweet, tweet_texts))



                # create links
                print("building links")
                df_direct_links = pd.concat(direct_links_frames)
                df_direct_links = df_direct_links.drop_duplicates()
                print("direct links are : ")
                print(df_direct_links)

                frames = DataIndirectLinkHelper.get_indirect_links(hashtags=hashtags_dict, urls=urls_dict, vocabularies=voc_frames)
                if len(frames) > 0 :
                    df_indirect_links = pd.concat(frames)

                if df_indirect_links.empty:
                    df_indirect_links = pd.DataFrame(columns=['userFromId', 'userToId'])
                else:
                    df_indirect_links = df_indirect_links.drop_duplicates()
                print("indirect links are : ")
                print(df_indirect_links)

                print("merging...")
                df_all_links = pd.DataFrame(columns=['userFromId', 'userToId'])
                bulid_direct_links = False
                bulid_indirect_links = False
                if not df_direct_links.empty:
                    df_all_links = pd.concat([df_direct_links])
                if not df_indirect_links.empty:
                    df_all_links = pd.concat([df_all_links, df_indirect_links])

                # save to reuse treatment
                print("saving...")
                redis_df_tag_direct_links = query + "_df_direct_links"
                redis_handler.save_dataframe_to_redis(dataframe=df_direct_links, redis_df_tag=redis_df_tag_direct_links)
                redis_df_tag_indirect_links = query + "_df_indirect_links"
                redis_handler.save_dataframe_to_redis(dataframe=df_indirect_links, redis_df_tag=redis_df_tag_indirect_links)
                redis_df_tag_all_links = query + "_df_all_links"
                redis_handler.save_dataframe_to_redis(dataframe = df_all_links, redis_df_tag = redis_df_tag_all_links)

                print("complete. Got to 3 to visualize")
        except Exception as e:
            print("Error : " + str(e))
            ans = False
    elif ans == "3":
        if redis_tweet_tag == "":
            print("Default subject : " + query )
        print("\nVisualization of subject " + query)

        redis_df_tag_direct_links = query + "_df_direct_links"
        redis_df_tag_indirect_links = query + "_df_indirect_links"
        redis_df_tag_all_links = query + "_df_all_links"

        df_redis_all_links = redis_handler.retrieve_dataframe(redis_df_tag_all_links)
        if df_redis_all_links.empty :
            print("unable to retrieve all links. it is empty")
        else:
            print(str(len(df_redis_all_links)) + " global links")

        df_redis_direct_links = redis_handler.retrieve_dataframe(redis_df_tag_direct_links)
        if df_redis_direct_links.empty:
            print("unable to retrieve direct links. it is empty")
        else:
            print(str(len(df_redis_direct_links)) + " direct links")

        df_redis_indirect_links = redis_handler.retrieve_dataframe(redis_df_tag_indirect_links)
        if df_redis_indirect_links.empty:
            print("unable to retrieve indirect links. it is empty")
        else:
            print(str(len(df_redis_indirect_links)) + " indirect links")

        graph_drawer = GraphDrawer("graph")
        graph_drawer.add_edges(df_redis_all_links)
        graph_drawer.add_nodes(df_redis_all_links)
        graph_drawer.draw_graph()

        print(graph_drawer.get_clique())
        print(graph_drawer.get_clusters())
        print(graph_drawer.get_triangles())
        trace1 = graph_drawer.scatter_nodes()
        trace2 = graph_drawer.scatter_edges()

        graph_drawer.create_iplot(trace1=trace1, trace2=trace2)

        graph_drawer.display_graph()




    elif ans == "q":
        redis_tweet_tag = ""
        print("\nGoodbye!")
        ans = False
    else:
        print("\nNot A Valid Choice Try again")





# print(json_tweets)
# print(search_tweets)
# for t in search_tweets:
#    print(t["user"]["name"])

# print("\n Hello")
# for tweet in search_tweets:
#  print(tweet.text)






# preTreatment
