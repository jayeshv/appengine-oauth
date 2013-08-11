from google.appengine.ext import db

from src.authentication.user import User
from src.authentication.oauth.provider.consumer import Consumer
from src import get_random_string

class Token(db.Model):
    token = db.StringProperty(default='')
    secret = db.StringProperty(default='')
    consumer = db.ReferenceProperty(Consumer)
    user = db.ReferenceProperty(User, required=False)
    created = db.DateTimeProperty(auto_now_add=True)
    callback = db.StringProperty()

    def generate_secret(self):
        self.secret = get_random_string()

    @staticmethod
    def create(token, consumer, callback):
        token.token = get_random_string()
        token.secret = get_random_string()
        token.consumer = consumer
        token.callback = callback

    @staticmethod
    def get_by_token(token):
        query = Token.all().filter('token', token)
        if query.count():
            return query[0]
        return None
