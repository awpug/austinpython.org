""" The utilities for autneticating / making twitter requests. """

import oauth2
import urllib
import urlparse
from austinpython import settings

def get_twitter_consumer(key=None, secret=None):
    """ Create the redirect url. """
    if not key:
        key = settings.TWITTER_CONSUMER_KEY
    if not secret:
        secret = settings.TWITTER_CONSUMER_SECRET
    consumer = oauth2.Consumer(key, secret)
    return consumer

def get_twitter_request_token(consumer=None):
    """ Retrieve a request token from Twitter. """
    if not consumer:
        consumer = get_twitter_consumer()
    client = oauth2.Client(consumer)
    request_token_url = "https://api.twitter.com/oauth/request_token"
    params = {"oauth_callback": settings.TWITTER_CALLBACK_URL}
    body = urllib.urlencode(params)
    request, content = client.request(request_token_url, "GET", body=body)
    if request.status != 200:
        raise Exception("Invalid Twitter token request: %s" % content)
    response_args = urlparse.parse_qs(content)
    assert(response_args["oauth_callback_confirmed"])
    token = oauth2.Token(key=response_args["oauth_token"][0],
                         secret=response_args["oauth_token_secret"][0])
    token.set_callback(settings.TWITTER_CALLBACK_URL)
    return token

def get_twitter_redirect_url(token=None):
    """ Returns the Twitter redirect url with the token. """
    if not token:
        token = get_twitter_request_token()
    url = "https://twitter.com/oauth/authorize"
    args = {"oauth_token": token.key,
            "oauth_callback": token.get_callback_url()}
    return url + "?" + urllib.urlencode(args)

