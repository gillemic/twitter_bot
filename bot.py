from tweepy import OAuthHandler, Stream, StreamListener, API, TweepError
import os
from dotenv import load_dotenv
import json
from pprint import pprint

load_dotenv()
API_KEY = os.getenv("API_KEY")
API_SECRET_KEY = os.getenv("API_SECRET_KEY")
BEARER_TOKEN = os.getenv("BEARER_TOKEN")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")

auth = OAuthHandler(API_KEY, API_SECRET_KEY)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

class StdOutListener(StreamListener):
    """ A listener handles tweets that are received from the stream.
    This is a basic listener that just prints received tweets to stdout.
    """
    def on_data(self, data):
        json_data = json.loads(data)
        tweet_id = json_data['id_str']
        author = json_data['user']['screen_name']
        is_reply = True if json_data['in_reply_to_screen_name'] != None else False

        with open('tweet_ids', 'a+') as t:
          if ((tweet_id + '\n') in t) or is_reply or (author != 'jon_bois'):
            return
          t.write(tweet_id + "\n")
          pprint(json_data)
          
        tweet_text = "@jon_bois"
        image_path = "./floral.jpg"
        api = API(auth)
        try:
          api.update_with_media(image_path, tweet_text, in_reply_to_status_id=int(tweet_id))
        except TweepError:
          print("Tweepy error!")
          return True

        return True

    def on_error(self, status):
        if status == 420:
            #returning False in on_data disconnects the stream
            print("error! status: " + str(status))
            #return False

if __name__ == '__main__':
    l = StdOutListener()
    #auth = OAuthHandler(API_KEY, API_SECRET_KEY)
    #auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    stream = Stream(auth, l)
    stream.filter(follow=["70739029"])