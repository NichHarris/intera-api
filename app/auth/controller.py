from os import environ as env
from dotenv import find_dotenv, load_dotenv
from functools import wraps
from six.moves.urllib.request import urlopen
from flask import _request_ctx_stack, request
from jose import jwt
import json

load_dotenv(find_dotenv())
AUTH0_CLIENT_SECRET = env.get('AUTH0_CLIENT_SECRET')

def get_auth_token(request):
    auth = request.headers.get('Authorization', None)
    token = auth.split(' ')[1] if auth else None

    return token

def get_rsa_key(token, jwks):
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    
    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }

    return rsa_key

def decode_jwt(token):
    BASE_URL = env.get('AUTH0_ISSUER_BASE_URL')
    jsonurl = urlopen(f'https://{BASE_URL}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())

    rsa_key = get_rsa_key(token, jwks)

    if rsa_key:
        payload = jwt.decode(
            token,
            rsa_key,
            algorithms=['RS256'],
            audience=env.get('AUTH0_AUDIENCE'),
            issuer=f'https://{BASE_URL}/'
        )

        return payload
    return None

def requires_auth(func):
    '''Determines if the access token is valid
    '''

    @wraps(func)
    def decorated(*args, **kwargs):
        token = get_auth_token(request)
        payload = decode_jwt(token)
        if payload:
            _request_ctx_stack.top.current_user = payload
            return func(*args, **kwargs)

    return decorated