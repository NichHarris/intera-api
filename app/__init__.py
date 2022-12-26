import json
from os import environ as env
from urllib.parse import quote_plus, urlencode

from authlib.integrations.flask_client import OAuth
from dotenv import find_dotenv, load_dotenv
from flask import Flask, redirect, render_template, session, url_for
from config import Config

# load .env file
load_dotenv(find_dotenv())

# get APP_SECRET_KEY from .env file
APP_SECRET_KEY = env.get("APP_SECRET_KEY")

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.secret_key = APP_SECRET_KEY

    # Initialize Flask extensions here

    # Register blueprints here
    from app.main import main
    app.register_blueprint(main, url_prefix='/')

    from app.auth import auth
    app.register_blueprint(auth, url_prefix='/auth')

    @app.route('/test/')
    def test_page():
        return '<h1>Testing the Flask Application Factory Pattern</h1>'

    return app