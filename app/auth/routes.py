import json
from os import environ as env
from urllib.parse import quote_plus, urlencode
from authlib.integrations.flask_client import OAuth
from dotenv import find_dotenv, load_dotenv
from flask import Flask, redirect, render_template, session, url_for

import app
from app.auth import auth
from config import Config


# create the Auth0 object
oauth = OAuth(app.create_app())

# create the Auth0 object
oauth.register(
    "auth0",
    client_id=Config.AUTH0_CLIENT_ID,
    client_secret=Config.AUTH0_CLIENT_SECRET,
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{Config.AUTH0_DOMAIN}/.well-known/openid-configuration'
)

oauth.register(
    "auth0",
    client_id=Config.AUTH0_CLIENT_ID,
    client_secret=Config.AUTH0_CLIENT_SECRET,
    api_base_url=f"https://{Config.AUTH0_DOMAIN}/",
    access_token_url=f"https://{Config.AUTH0_DOMAIN}/oauth/token",
    authorize_url=f"https://{Config.AUTH0_DOMAIN}/authorize",
    client_kwargs={
        "scope": "openid profile email",
    },
)

@auth.route('/login')
def login():
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("main.index", _external=True)
    )

@auth.route('/callback')
def callback():
    oauth.auth0.authorize_access_token()
    resp = oauth.auth0.get('userinfo')
    userinfo = resp.json()
    session['jwt_payload'] = userinfo
    session['profile'] = {
        'user_id': userinfo['sub'],
        'name': userinfo['name'],
        'picture': userinfo['picture']
    }
    return redirect('/dashboard')

@auth.route("/register")
def register():
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("auth.callback", _external=True),
        audience=f"https://{Config.AUTH0_DOMAIN}/api/v2/",
    )


# @auth.route("/callback", methods=["GET", "POST"])
# def callback():
#     token = oauth.auth0.authorize_access_token()
#     session["user"] = token
#     return redirect("/")

@auth.route("/logout")
def logout():
    session.clear()
    return redirect(
        "https://" + Config.AUTH0_DOMAIN
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": url_for("home", _external=True),
                "client_id": Config.AUTH0_CLIENT_ID,
            },
            quote_via=quote_plus,
        )
    )