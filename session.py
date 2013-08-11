import uuid

from google.appengine.ext import db

from src.authentication.user import User

class Session(db.Model):
    user = db.ReferenceProperty(User)
    token = db.StringProperty()
    created = db.DateTimeProperty(auto_now_add=True)

    @staticmethod
    def get_by_token(session_token):
        query = Session.all().filter('token', session_token)
        if query.count():
            return query[0]
        return None

    @staticmethod
    def create(session, user):
        session.user = user
        session.token = str(uuid.uuid1())
