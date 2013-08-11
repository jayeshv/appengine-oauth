from google.appengine.ext import webapp

from src.authentication.oauth import get_base_string
from src.authentication.oauth.provider.consumer import Consumer
from src.authentication.oauth.provider.token import Token
from src.authentication.oauth import validate_signature
from src.authentication.oauth import get_oauth_params

class RequestTokenHandler(webapp.RequestHandler):

    def get(self):
        pass

    def post(self):
        oauth_params = get_oauth_params(self.request)
        consumer = Consumer.get_by_consumer_key(oauth_params['oauth_consumer_key'])
        signature = oauth_params['oauth_signature']
        oauth_params.pop('oauth_signature')
        oauth_params.pop('realm')
        base_string = get_base_string(oauth_params, self.request.url, 'POST')
        callback = oauth_params.get("oauth_callback", consumer.callback)
        if validate_signature(consumer, base_string, signature):
            token = Token()
            Token.create(token, consumer, callback)
            token.put()
            self.response.out.write("oauth_token=%s&oauth_token_secret=%s" % (token.token,
                                                                              token.secret))
