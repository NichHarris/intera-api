from os import environ as env
from dotenv import find_dotenv, load_dotenv
from urllib.parse import quote_plus, urlencode
from authlib.integrations.flask_client import OAuth
from auth0.v3.authentication import Users, GetToken
from flask import Flask, redirect, render_template, session, url_for, request, jsonify

from authlib.integrations.flask_oauth2 import ResourceProtector


import app
from app.auth import auth
from config import Config

load_dotenv(find_dotenv())
AUTH0_CLIENT_SECRET = env.get("AUTH0_CLIENT_SECRET")

require_auth = ResourceProtector()

# create the Auth0 object
oauth = OAuth(app.create_app())

oauth.register(
    "auth0",
    client_id=env.get("AUTH0_CLIENT_ID"),
    client_secret=env.get("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
)

def get_user_info():
    user_info = oauth.auth0.get("userinfo").json()
    return user_info

def get_auth_header():
    header = request.headers.get("Authorization", None)

    if not header:
        return jsonify(error="Authorization header is expected", status=401)
    
    header_split = header.split()

    if header_split[0].lower() != "bearer":
        return jsonify(error="Authorization header must start with Bearer", status=401)

    elif len(header_split) == 1:
        return jsonify(error="Token not found", status=401)
    
    return jsonify(message="success", data={'token': header_split[1]}, status=200)


# verify if logged in and then redirect here if not
@auth.route('/login')
def login():
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("main.index", _external=True)
    )

@auth.route("/callback", methods=["GET", "POST"])
# need to check what url the user was accessing from
def callback():
    token = oauth.auth0.authorize_access_token()
    session["user"] = token

    # authenticate the user
    get_token = GetToken(Config.AUTH0_DOMAIN)
    user_info = get_token.client_credentials(
        Config.AUTH0_CLIENT_ID, AUTH0_CLIENT_SECRET, audience=Config.AUTH0_AUDIENCE
    )
    print(user_info)
    return redirect(
        "https://" + Config.AUTH0_DOMAIN
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": url_for("main.index", _external=True),
                "client_id": Config.AUTH0_CLIENT_ID,
            },
            quote_via=quote_plus,
        )
    )

@auth.route("/logout")
def logout():
    session.clear()
    return redirect(
        "https://" + Config.AUTH0_DOMAIN
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": url_for("main.index", _external=True),
                "client_id": Config.AUTH0_CLIENT_ID,
            },
            quote_via=quote_plus,
        )
    )