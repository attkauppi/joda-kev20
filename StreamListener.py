# -*- coding:utf-8 -*-
import tweepy
import sys
import os
import time
import dataset

# Based on: https://www.storybench.org/how-to-collect-tweets-from-the-twitter-streaming-api-using-python/

# Stream listener class inherits from tweepy.StreamListener and overrides on_status/on_error methods:
class StreamListener(tweepy.StreamListener):
    def on_status(self, status):
        """
        To avoid seeing the same tweets over and over again due to people retweeting them, we want to
        check an attribute called retweet_status in the status object.
        """
        
        print(status.id_str)

        # Handling retweets
        ## If retweeted_status attribute exists, flag tweet as a retweet
        text = ""
        is_retweet = False
        if hasattr(status, "retweeted_status"):
            is_retweet = True
            #if hasattr(status.retweeted_status, "extended_tweet"):
            #    text = status.retweeted_status.extended_tweet["full_text"]
            #else:
            #    text = status.retweeted_status.text

        #text = ""
        # Check if text is truncated
        if hasattr(status,"extended_tweet"):
            text = status.extended_tweet["full_text"]
        else:
            text = status.text
      
        # Check if this is a quote tweet
        is_quote = False
        is_quote = hasattr(status, "quoted_status")
        quoted_text = ""
        if is_quote:
            # Check if quoted tweet's text has been truncated before rcording
            if hasattr(status.quoted_status,"extended_tweet"):
                quoted_text = status.quoted_status.extended_tweet["full_text"]
            else:
                quoted_text = status.quoted_status.text
    
        # Remove characters that might cause problems with csv encoding
        remove_characters = [",","\n"]
        for c in remove_characters:
            text.replace(c, " ")
            quoted_text.replace(c, " ")


        lang = ""
        lang = status.lang
        print("LANG: ", lang)
	# Recording in an sqlite3 database
        db = dataset.connect("sqlite:///tweets2.db")
        table = db["tweets"]
        print(text)
        table.insert(dict(
            created_at = status.created_at,
            tweet_id = status.id_str,
            user_id = status.user.id_str,
            screen_name = status.user.screen_name,
            is_retweet = is_retweet,
            is_quote = is_quote,
            text = text,
            quoted_text = quoted_text,
            lang = lang,))

        hashtag_list = []
        if hasattr(status, "entities"):
            entities = status.entities
            if "hashtags" in entities:
                for hashtag in entities["hashtags"]:
                    if "text" in hashtag and hashtag is not None:
                        #if hashtag is not None and "text" in hashtag:
                        hashtag = hashtag["text"]
                        hashtag_list.append(hashtag)
                    #if "text" in hashtag:
                    #    hashtag = hashtag["text"]
                    #    if hashtag is not None:
                    #    hashtag_list.append(hashtag)
#status.entities.hashtags
        table_hashtags = db["hashtags"]

        print("Tulostaa viestin hashtagit: ")
        for i in hashtag_list:
            print(i.lower())

        for i in hashtag_list:
            i = i.lower()
            print("tagi i: ", i)
            tagi = table_hashtags.find_one(hashtag=i)
            print("onko tietokannassa? ", tagi)
            if tagi is None:
                table_hashtags.insert(dict(hashtag=i,esiintynyt=1,))
            else:
                tagi = table_hashtags.find_one(hashtag=i)
                print("tagin nimi: ", tagi["hashtag"])
                print("Tagin esiintymiskerrat ennen viimeisinta: ", tagi['esiintynyt'])
                esiintymiskerrat = tagi['esiintynyt']
                esiintymiskerrat = esiintymiskerrat + 1
                table_hashtags.update(dict(hashtag=tagi["hashtag"], esiintynyt=esiintymiskerrat), ["hashtag"])
            tagi = table_hashtags.find_one(hashtag=i)
            print("tagi_id: ", tagi['id'])
            tagi_id = tagi['id']
            tweet_tags_table = db['tweet_tags']
            tweet_tags_table.insert(dict(
                tweet_id =status.id_str,
                tag_id = tagi_id,))

            print(i)
        print("----")

        #table_hashtags = db["hashtags"]

        #table_hashtags.insert
        # Recording tweet information in out.csv
        #with open(self.output_filename, "a", encoding='utf-8') as f:
        with open("out.csv", "a", encoding='utf-8') as f:
            f.write("%s,%s,%s,%s,%s,%s\n" % (status.created_at,status.user.screen_name,is_retweet,is_quote,text,quoted_text))


    def on_error(self, status_code):
        if status_code == 420:
            # 420 error means that we've been making too many requests too fast,
            # so it's time to take short break.
            print("Encountered a 420 error")
            time.sleep(120)
        else:
            print("Encountered streaming error (", status_code, ")")
            sys.exit()
    
if __name__ == "__main__":

    consumer_key = ""
    consumer_secret = ""
    access_key = ""
    access_secret = ""

    # Reading access tokens from a file, which is NOT pushed to github! Alternatively, if we're in
    # the heroku environment, these will be stored in heroku as environment variables.
    ## ==> Not properly implemented yet for Heroku deployments and that may not be useful anyway.



    # Finding out whether we're running the program locally or on heroku
    if os.environ.get("HEROKU"):
        #Do something
        print("Herokussa ollaan")
    else:
        # The keys etc. are stored in auth.conf in the following order:
        # consumer_key, consumer_secret, access_key, access_secret, all of them on their
        # own respective lines.
        f = open('auth.conf', "r")
        lines = f.readlines()
        print(lines)

        consumer_key = lines[0].strip()
        consumer_secret = lines[1].strip()
        access_key = lines[2].strip()
        access_secret = lines[3].strip()

        print(consumer_key)
        print(consumer_secret)
        print(access_key)
        print(access_secret)

        f.close()


    # Auth and initializing API endpoint
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

    # Initialize stream
    streamListener = StreamListener()
    stream = tweepy.Stream(auth=api.auth, listener=streamListener, tweet_mode='extended')

    tags = ['etätyö']
    stream.filter(track=tags)
