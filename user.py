from google.appengine.ext import db
from django.utils import simplejson

class User(db.Model):
    provider = db.StringProperty()
    id = db.StringProperty()
    name = db.StringProperty()
    avatar = db.StringProperty()

    def dump(self, format='json'):
        dump = {'name': self.name, 'id': self.key().id(),
                'provider': self.provider, 'avatar': self.avatar}
        if format == 'josn':
            return simplejson.dumps(dump)
        elif format == 'data':
            return dump
        else:
            return simplejson.dumps(dump)

    @staticmethod
    def get(provider, id):
        query = User.all().filter('provider', provider).filter('id', id)
        if query.count():
            return query[0]
        return None

    @staticmethod
    def create(user, provider, id, name, avatar=''):
        user.provider = provider
        user.id = id
        user.name = name
        user.avatar = avatar
