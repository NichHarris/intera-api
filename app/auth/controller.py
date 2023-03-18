# Environment variables
from os import environ as env
from dotenv import find_dotenv, load_dotenv

# Flask
from flask import _request_ctx_stack, request, jsonify

# Auth0
from jose import jwt, ExpiredSignatureError

# Utilities
from functools import wraps
import http.client
from six.moves.urllib.request import urlopen
import json

load_dotenv(find_dotenv())
AUTH0_CLIENT_SECRET = env.get('AUTH0_CLIENT_SECRET')

def get_auth_token(request=request):
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

def get_management_token():
    conn = http.client.HTTPSConnection("")

    CLIENT_ID = env.get('AUTH0_CLIENT_ID')
    CLIENT_SECRET = env.get('AUTH0_CLIENT_SECRET')
    DOMAIN = env.get('AUTH0_ISSUER_BASE_URL')

    payload = f"grant_type=client_credentials&client_id={CLIENT_ID}&client_secret={CLIENT_SECRET}&audience=https://{DOMAIN}/api/v2/"

    headers = { 'content-type': "application/json" }

    conn.request("POST", f"https://{DOMAIN}/oauth/token", payload, headers)

    res = conn.getresponse()
    data = res.read()

    return data.decode("utf-8")

def management_api_user():
    conn = http.client.HTTPSConnection("")
    yourMgmtApiAccessToken = ''
    headers = { 'authorization': f"Bearer {yourMgmtApiAccessToken}" }
    email = ''
    conn.request("GET", f"/YOUR_DOMAIN/api/v2/users?q=email={email}&search_engine=v3", headers=headers)

    res = conn.getresponse()
    data = res.read()

    print(data.decode("utf-8"))

def decode_jwt(token):
    BASE_URL = env.get('AUTH0_ISSUER_BASE_URL')
    jsonurl = urlopen(f'https://{BASE_URL}/.well-known/jwks.json')

    # JSON Web Token key set
    jwks = json.loads(jsonurl.read())

    rsa_key = get_rsa_key(token, jwks)

    if rsa_key:
        payload = jwt.decode(
            token,
            rsa_key,
            algorithms=['RS256'],
            audience=env.get('AUTH0_CLIENT_ID'),
            issuer=f'https://{BASE_URL}/'
        )

        if payload['iss'] != f'https://{BASE_URL}/':
            return jsonify(error='401 - Unauthorized Invalid issuer', status=401)

        return payload
    return None

def requires_auth(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = get_auth_token(request)
        if not token:
            return jsonify(error='401 - Authorization header is expected', status=401)

        try:
            payload = decode_jwt(token)
        except ExpiredSignatureError:
            return jsonify(error='401 - Token expired, reauthentication required', status=401)


        if 'error' in payload:
            return jsonify(error=payload['error'], status=payload['status'])

        if payload:
            _request_ctx_stack.top.current_user = payload
            return func(*args, **kwargs)

    return decorated