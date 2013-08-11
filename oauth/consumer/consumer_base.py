import cgi

from src.authentication.oauth.consumer import oauth_request

class ConsumerBase(object):

    def __init__(self, oauth_token='', oauth_secret=''):
        self.oauth_token = oauth_token
        self.oauth_secret = oauth_secret

    def get_authorize_url(self):
        request = oauth_request.OauthRequest(self, self.request_token_url, method='POST',
                                             additional_oauth_params={"oauth_callback": self.callback_url})
        response = request._fetch().content
        dic = cgi.parse_qs(response)
        oauth_token = dic['oauth_token'][0]
        oauth_secret = dic['oauth_token_secret'][0]
        return '%s?oauth_token=%s' %(self.authorize_url, oauth_token)

    def set_access_token(self):
        request = oauth_request.OauthRequest(self, self.access_token_url, method='POST')
        response = request._fetch().content
        dic = cgi.parse_qs(response)
        self.oauth_token = dic['oauth_token'][0]
        self.oauth_secret = dic['oauth_token_secret'][0]

    def _get_oauth_verifier(self):
        return self.oauth_secret

    def _get_oauth_token(self):
        return self.oauth_token

    def _get_key(self):
        return self.consumer_key

    def _get_consumer_secret(self):
        return self.consumer_secret

    def get_user_info(self):
        request = oauth_request.OauthRequest(self, self.user_info_url)
        response = request._fetch().content
        return response
