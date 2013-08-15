from src.authentication.oauth.consumer import consumer_base

CONSUMER_KEY = ''
CONSUMER_SECRET = ''
REQUEST_TOKEN_URL = 'https://api.twitter.com/oauth/request_token'
AUTHORIZE_URL = 'https://api.twitter.com/oauth/authorize'
ACCESS_TOKEN_URL = 'https://api.twitter.com/oauth/access_token'
CALLBACK_URL = 'http://localhost:8080/api/provider_authorize/'
USER_INFO_URL = 'http://api.twitter.com/1/account/verify_credentials.json'

class TwitterConsumer(consumer_base.ConsumerBase):

    def __init__(self, oauth_token='', oauth_secret=''):
        super(TwitterConsumer, self).__init__(oauth_token, oauth_secret)
        self.consumer_key = CONSUMER_KEY
        self.consumer_secret = CONSUMER_SECRET
        self.request_token_url = REQUEST_TOKEN_URL
        self.authorize_url = AUTHORIZE_URL
        self.access_token_url = ACCESS_TOKEN_URL
        self.callback_url = CALLBACK_URL
        self.user_info_url = USER_INFO_URL
