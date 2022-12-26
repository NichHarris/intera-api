from os import environ as env
from urllib.parse import quote_plus, urlencode
from authlib.integrations.flask_client import OAuth
from dotenv import find_dotenv, load_dotenv
from flask import Flask, redirect, render_template, session, url_for

import app
from app.auth import auth
from config import Config

load_dotenv(find_dotenv())
AUTH0_CLIENT_SECRET = env.get("AUTH0_CLIENT_SECRET")

# create the Auth0 object
oauth = OAuth(app.create_app())

oauth.register(
    "auth0",
    client_id=Config.AUTH0_CLIENT_ID,
    client_secret=AUTH0_CLIENT_SECRET,
    api_base_url=f"https://{Config.AUTH0_DOMAIN}/",
    access_token_url=f"https://{Config.AUTH0_DOMAIN}/oauth/token",
    authorize_url=f"https://{Config.AUTH0_DOMAIN}/authorize",
    client_kwargs={
        "scope": "openid profile email",
    },
)

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
    # session["userinfo"] = json.loads(
    #     oauth.auth0.get("userinfo").text
    # )
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