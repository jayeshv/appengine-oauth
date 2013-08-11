from google.appengine.ext import db

from src.authentication.oauth.provider.token import Token
from src.authentication.oauth.provider.consumer import Consumer
from src.authentication.user import User
from src import get_random_string

class AccessToken(db.Model):
    token = db.StringProperty(default='')
    secret = db.StringProperty(default='')
    request_token = db.ReferenceProperty(Token, required=False)
    consumer = db.ReferenceProperty(Consumer, required=False)
    user = db.ReferenceProperty(User)
    created = db.DateTimeProperty(auto_now_add=True)

    @staticmethod
    def create(token, user, request_token=None):
        token.token = get_random_string()
        token.secret = get_random_string()
        token.user = user
        if request_token:
            token.request_token = request_token
            token.consumer = request_token.consumer

    @staticmethod
    def get_by_token(token):
        query = AccessToken.all().filter('token', token)
        if query.count():
            return query[0]
        return None
