from constants.Constants import *
from database.RedisHandler import RedisHandler
from config.Authentication import Authentication
from tweeterAnalyse.DataCapture import DataCapture
from tweeterAnalyse.DataPreTreatment import DataPreTreatment
import json

# auth = Authentication()
# tweeter_capture = TweetCapture()
# tweeter_pre_treatment = DataPreTreatment()
redis_handler = RedisHandler()

# authenticate to tweeter
api = Authentication.auth(consumer_key=CONSUMER_KEY, consumer_secret=CONSUMER_SECRET, access_token=ACCESS_TOKEN,
                access_token_secret=ACCESS_TOKEN_SECRET)

ans = True
redis_tweet_tag = ""
query = 'espion'
while ans:
    print("""
    1.Look for a subject (Default : "espion")
    2.Analyse subject
    q.Exit/Quit
    """)
    ans = input("What would you like to do? ")
    if ans == "1":
        print("\nLook for a subject ")
        # get tweets
        max_tweets = 50
        query_bis = input("Type a subject : (Press Enter for Default) ")
        if query_bis == "":
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
            print("Default subject : espion")
            redis_tweet_tag = "tweets_query_" + query
        print("\nAnalyse of subject " + query)
        try:
            tweets = json.loads(redis_handler.retrieve_tweets(redis_tweet_tag=redis_tweet_tag))
            if not tweets:
                print("\nUnable to load payload. Please Look for a subject again.")
            else:
                print(tweets)
                for i in tweets:
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

        except Exception as e:
            print("Error : " + str(e))
            ans = False
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
