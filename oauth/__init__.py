from base64 import b64encode
from hashlib import sha1
import hmac
from urlparse import urlparse
from urllib import quote

def get_oauth_params(request):
    authorization_header = request.headers['Authorization']
    oauht_header = authorization_header.split(' ')
    oauth_params = None
    if oauht_header[0] == 'OAuth':
        oauth_params = dict([each.split('=') for each in oauht_header[1].split(',')])
    return oauth_params        

def get_base_string(auth_params, url, method='GET'):
    pu = urlparse(urlparse(url).geturl())
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
        method,
        quote(normUrl, ''),
        oauth_params
        )
    return sig

def validate_signature(consumer, base_string, given_signature, token=None):
    if token:
        key = "%s&%s" % (quote(consumer.consumer_secret.encode('utf-8'), ''),
                         quote(token.secret.encode('utf-8'), ''))
    else:
        key = "%s&%s" % (quote(consumer.consumer_secret.encode('utf-8'), ''), 
                         quote(''))
    signature = quote(b64encode(hmac.new(key, base_string, sha1).digest()).encode('utf-8'))
    if signature == given_signature:
        return True
    return False
