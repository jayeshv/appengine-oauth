from base64 import b64encode
from hashlib import sha1
import hmac
from urllib import quote

from google.appengine.ext import webapp

from src.authentication.oauth.provider.consumer import Consumer
from src.authentication.oauth.provider.token import Token
from src.authentication.oauth.provider.access_token import AccessToken
from src.authentication.oauth import get_base_string
from src.authentication.oauth import validate_signature
from src.authentication.oauth import get_oauth_params

class AccessTokenHandler(webapp.RequestHandler):

    def get(self):
        pass

    def post(self):
        oauth_params = get_oauth_params(self.request)
        consumer = Consumer.get_by_consumer_key(oauth_params['oauth_consumer_key'])
        signature = oauth_params['oauth_signature']
        oauth_params.pop('oauth_signature')
        oauth_params.pop('realm')
        consumer = Consumer.get_by_consumer_key(oauth_params['oauth_consumer_key'])
        token = Token.get_by_token(oauth_params['oauth_token'])
        base_string = get_base_string(oauth_params, self.request.url, 'POST')
        if validate_signature(consumer, base_string, signature, token):
            access_token = AccessToken()
            AccessToken.create(access_token, token.user, token)
            access_token.put()
            self.response.out.write("oauth_token=%s&oauth_token_secret=%s" %(access_token.token,
                                                                             access_token.secret))
