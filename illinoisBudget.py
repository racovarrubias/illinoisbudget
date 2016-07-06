import os

TWITTER_CONSUMER_KEY = os.environ.get('TWITTER_CONSUMER_KEY')
TWITTER_CONSUMER_SECRET = os.environ.get('TWITTER_CONSUMER_SECRET')
TWITTER_ACCESS_KEY = os.environ.get('TWITTER_ACCESS_KEY')
TWITTER_ACCESS_SECRET = os.environ.get('TWITTER_ACCESS_SECRET')

hashtag = '#IllinoisBudget'
tweets_file_name = 'illinoisBudget_tweets.csv'
tweets_quantity = 5000

import tweepy
from time import clock, sleep
import csv

auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
auth.set_access_token(TWITTER_ACCESS_KEY, TWITTER_ACCESS_SECRET)
api = tweepy.API(auth)

start = clock()
with open(tweets_file_name, 'w') as f:
    writer = csv.writer(f)

    class StreamListener(tweepy.StreamListener):

        collected_tweets = 0

        def on_status(self, status):
            try:
                tweet = status.text
                tweet = tweet.replace('\n', '\\n')
                timePass = clock() - start
                if timePass % 60 == 0:
                    print ("I have been working for", timePass, "seconds.")
                if not ('RT @' in tweet):  # Exclude re-tweets
                    writer.writerow([tweet])
                    self.collected_tweets += 1
                    if self.collected_tweets % 1000 == 0:
                        print ("I have collected", self.collected_tweets, "tweets!")
                    if self.collected_tweets == tweets_quantity:
                        print ("I have finished!")
                        return False
                    pass

            except Exception as e:
                sys.stderr.write('Encountered Exception:' + str(e))
                pass

        def on_error(self, status_code):
            print('Error: ' + repr(status_code))
            return True  # False to stop

        def on_delete(self, status_id, user_id):
            """Called when a delete notice arrives for a status"""
            print("Delete notice for" + str(status_id) + '. ' + str(user_id))
            return

        def on_limit(self, track):
            """Called when a limitation notice arrives"""
            return

        def on_timeout(self):
            """Called when there is a timeout"""
            sys.stderr.write('Timeout...')
            sleep(10)
            return True

    streamingAPI = tweepy.streaming.Stream(auth, StreamListener())
    streamingAPI.filter(track=[hashtag])
