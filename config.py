import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    AUTH0_CLIENT_ID='YfFXlkN6VSJtKISCKRrUNUdqPDjp5oZb'
    AUTH0_DOMAIN='dev-gsbv87qpmgwdpjej.us.auth0.com'
    AUTH0_CALLBACK_URL='http://localhost:5000/callback'
    AUTH0_AUDIENCE='http://localhost:5000/'