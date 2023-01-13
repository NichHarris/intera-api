from os import environ as env
from dotenv import find_dotenv, load_dotenv
from functools import wraps
from six.moves.urllib.request import urlopen
import json

from typing import Dict

from flask import Flask, request, jsonify, _request_ctx_stack, Response
from flask_cors import cross_origin
from jose import jwt

from flask import Flask, redirect, render_template, session, url_for, request, jsonify

load_dotenv(find_dotenv())
AUTH0_CLIENT_SECRET = env.get("AUTH0_CLIENT_SECRET")

def get_rsa_key(token, jwks):
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    
    for key in jwks["keys"]:
        if key["kid"] == unverified_header["kid"]:
            rsa_key = {
                "kty": key["kty"],
                "kid": key["kid"],
                "use": key["use"],
                "n": key["n"],
                "e": key["e"]
            }

    return rsa_key

def decode_jwt(token):
    jsonurl = urlopen("https://" + env.get('AUTH0_ISSUER_BASE_URL') + "/.well-known/jwks.json")
    jwks = json.loads(jsonurl.read())

    rsa_key = get_rsa_key(token, jwks)

    if rsa_key:
        payload = jwt.decode(
            token,
            rsa_key,
            algorithms=["RS256"],
            audience=env.get('AUTH0_AUDIENCE'),
            issuer="https://" + env.get('AUTH0_ISSUER_BASE_URL') + "/"
        )

        return payload
    return None

def requires_auth(func):
    """Determines if the access token is valid
    """

    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization').split(' ')[1]
        payload = decode_jwt(token)
        if payload:
            _request_ctx_stack.top.current_user = payload
            return func(*args, **kwargs)

    return decorated