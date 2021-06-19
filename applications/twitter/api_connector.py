import tweepy

api_key = 'l3sQl2GGtEQyghz5p5m6hmP1F'
api_secret_key = 'O7hjunhMYZ8mtlK88d20Cu4DtDV7iAcoKoSaoxc52ai2kcYSzp'
bearer_token = 'AAAAAAAAAAAAAAAAAAAAAJFlQgEAAAAAt7hON8jx%2BEr4a35ZLPoChpWXZCo%3DtTt36MbJDpy7oycmhUwrGBbEmqSK5ngTFNBRWAVJSbskGtGrgv'
access_token = '1342406315382099971-X1wKW4EAo6TH7ULysWDITp7SOdqdbW'
access_token_secret = 'wuxGjBQHqXnR0oAuCzWcS6iS2nTo4Wfn8cWRO2qpHgFs5'

auth = tweepy.OAuthHandler(api_key, api_secret_key)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)


class MyStreamListener(tweepy.StreamListener):
    def __init__(self, api):
        self.api = api
        self.me = api.me()

    def on_status(self, tweet):
        print(f"{tweet.user.name}:{tweet.text}")

    def on_error(self, status):
        print("Error detected")


tweets_listener = MyStreamListener(api)
stream = tweepy.Stream(api.auth, tweets_listener)
stream.filter(track=["Chelsea"], languages=["en"])