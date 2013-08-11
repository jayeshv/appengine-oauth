import time
import urllib
import string
import hmac
import random
from hashlib import sha1
from urllib import quote
from base64 import b64encode
from urlparse import urlparse

from google.appengine.api import urlfetch

class OauthRequest(object):

    def __init__(self, consumer, url, method='GET', headers={}, params={},
                 additional_oauth_params={}, signature_method="HMAC-SHA1"):
        self.consumer = consumer
        self.url = url
        self.headers = headers
        self.params = params
        self.additional_oauth_params = additional_oauth_params
        self.signature_method = signature_method
        self.method = method
        self.authenticate()

    def authenticate(self):
        auth_params = self._get_oauth_params()
        base_string = self._get_base_string(auth_params)
        signature = self._get_signature(base_string)
        auth_params['oauth_signature'] = signature
        auth_values = ['%s=%s' % (k[0], k[1]) for k in auth_params.iteritems()]
        self._set_auth_header(auth_values)

    def _get_oauth_params(self):
        auth_params = {"oauth_consumer_key": self.consumer._get_key(),
                       "oauth_nonce": self._get_nonce(),
                       "oauth_timestamp": self._get_time_stamp(),
                       "oauth_signature_method": self.signature_method,
                       "oauth_version": "1.0"}
        if self.consumer._get_oauth_token():
            auth_params['oauth_token'] = self.consumer._get_oauth_token()
        if self.consumer._get_oauth_verifier():
            auth_params['oauth_verifier'] = self.consumer._get_oauth_verifier()
        for key, value in self.params.iteritems():
            auth_params[key] = value
        for key, value in self.additional_oauth_params.iteritems():
            auth_params[key] = value
        return auth_params

    def _set_auth_header(self, auth_values):
        auth_header = 'OAuth realm="",' + ','.join(auth_values)
        self.headers["Content-type"] = "application/x-www-form-urlencoded"
        self.headers["Authorization"] = auth_header

    def _get_nonce(self, length=10):
        return ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(length))

    def _get_time_stamp(self):
        return str(int(time.time()))

    def _fetch(self):
        if self.method == 'GET':
            if self.params:
                self.url = self.url + '?' + '&'.join(['%s=%s' % param for param in self.params.iteritems()])
            result = urlfetch.fetch(url=self.url, headers=self.headers)
        elif self.method == 'POST':
            result = urlfetch.fetch(url=self.url,
                                    payload=urllib.urlencode(self.params),
                                    method=self.method,
                                    headers=self.headers)
        else:
            result = ''
        return result

    def _get_signature(self, base_string):
        if self.signature_method == 'HMAC-SHA1':
            key = "%s&%s" % (quote(self.consumer._get_consumer_secret().encode('utf-8'), ''),
                             quote(self.consumer._get_oauth_verifier().encode('utf-8'), ''))
            signature = quote(b64encode(hmac.new(key, base_string, sha1).digest()).encode('utf-8'))
        else:
            raise TypeError, "Signature method not supported"
        return signature

    def _get_base_string(self, auth_params):
        pu = urlparse(urlparse(self.url).geturl())
        normUrl = "%s://%s%s%s" % (
            pu.scheme,
            pu.hostname,
            "" if not pu.port or {"http":80,"https":443}[pu.scheme] == pu.port else ":%d" % pu.port,
            pu.path,
            )
        names = auth_params.keys()
        names.sort()
        auth_values = ['%s=%s' % (k[0], k[1]) for k in auth_params.iteritems()]
        oauth_params = quote("&".join(["%s=%s" % (k, quote(auth_params[k].encode('utf-8'), '')) for k in names]), '')
        sig = "%s&%s&%s" % (
            self.method.upper(),
            quote(normUrl, ''),
            oauth_params
        )
        return sig
