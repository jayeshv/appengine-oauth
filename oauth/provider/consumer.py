from google.appengine.ext import db

from src import get_random_string
from src.authentication.user import User

class Consumer(db.Model):
    consumer_key = db.StringProperty()
    consumer_secret = db.StringProperty()
    owner = db.ReferenceProperty(User)
    callback = db.StringProperty(default='')

    @staticmethod
    def create(consumer, user, callback):
        consumer.consumer_key = get_random_string(30)
        consumer.consumer_secret = get_random_string(40)
        consumer.owner = user
        consumer.callback = callback

    @staticmethod
    def get_by_consumer_key(key):
        query = Consumer.all().filter('consumer_key', key)
        if query.count():
            return query[0]
        return None
