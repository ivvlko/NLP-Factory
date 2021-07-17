import tweepy
import os
from dotenv import load_dotenv
load_dotenv()

api_key = os.environ.get('API_KEY')
api_secret_key = os.environ.get('API_SECRET_KEY')
bearer_token = os.environ.get('BEARER_TOKEN')
access_token = os.environ.get('ACCESS_TOKEN')
access_token_secret = os.environ.get('ACCESS_TOKEN_SECRET')


auth = tweepy.OAuthHandler(api_key, api_secret_key)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

