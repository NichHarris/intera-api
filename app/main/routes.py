from app.main import main
from app.auth import auth
from os import environ as env
from auth0.v3.authentication import Users, GetToken
from authlib.integrations.flask_oauth2 import ResourceProtector
# from validator import Auth0JWTBearerTokenValidator
from flask import render_template, session, redirect, url_for
from config import Config
from db import DB

AUTH0_CLIENT_SECRET = env.get("AUTH0_CLIENT_SECRET")
database = DB()

@main.route('/')
def index():

    # authenticate the user
    get_token = GetToken(Config.AUTH0_DOMAIN)
    # user_info = get_token.client_credentials(
    #     Config.AUTH0_CLIENT_ID, AUTH0_CLIENT_SECRET, audience=Config.AUTH0_AUDIENCE
    # )

    rand = database.retrieve_random_word()
    print(rand)
    if rand:
        print("word retrieved" )
    else:
        print("word not retrieved")
    # print(user_info)
    if session:
        return render_template('home.html')
    else:
        # redirect to login
        return redirect(url_for('auth.login'))
