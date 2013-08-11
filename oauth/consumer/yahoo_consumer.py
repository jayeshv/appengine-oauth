from src.authentication.oauth.consumer import consumer_base
from src import DOMAIN

CONSUMER_KEY = 'dj0yJmk9TjVMMmFIMVQ4aUpOJmQ9WVdrOVpFMDRWV0ZWTlRBbWNHbzlNVFUzTVRJeE56QTJNZy0tJnM9Y29uc3VtZXJzZWNyZXQmeD03ZA--'
CONSUMER_SECRET = '9c748815430723658682dd4e9a44cf8f9ddd1bbe'
REQUEST_TOKEN_URL = 'https://api.login.yahoo.com/oauth/v2/get_request_token'
AUTHORIZE_URL = 'https://api.login.yahoo.com/oauth/v2/request_auth'
ACCESS_TOKEN_URL = 'https://api.login.yahoo.com/oauth/v2/get_token'
CALLBACK_URL = '/oauth/provider_authorize/'
USER_INFO_URL = 'http://api.twitter.com/1/account/verify_credentials.json'

class YahooConsumer(consumer_base.ConsumerBase):

    def __init__(self, oauth_token='', oauth_secret='', client_token=''):
        super(YahooConsumer, self).__init__(oauth_token, oauth_secret)
        self.consumer_key = CONSUMER_KEY
        self.consumer_secret = CONSUMER_SECRET
        self.request_token_url = REQUEST_TOKEN_URL
        self.authorize_url = AUTHORIZE_URL
        self.access_token_url = ACCESS_TOKEN_URL
        self.callback_url = DOMAIN + CALLBACK_URL
        if client_token:
            self.callback_url = self.callback_url + '?client_token=' + client_token
        self.user_info_url = USER_INFO_URL
