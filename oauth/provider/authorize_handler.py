import os

from google.appengine.ext.webapp import template
from google.appengine.ext import webapp

from src.authentication.oauth.provider.token import Token

class AuthorizeHandler(webapp.RequestHandler):

    def get(self):
        oauth_token = self.request.get('oauth_token')
        token = Token.get_by_token(oauth_token)
        if token:
            path = os.path.join('views', 'login.html')
            self.response.out.write(template.render(path, {'client_token': token.token}))

    def post(self):
        pass
