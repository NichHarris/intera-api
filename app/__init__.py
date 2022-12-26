from os import environ as env
from dotenv import find_dotenv, load_dotenv
from flask import Flask
from config import Config

# load .env file
load_dotenv(find_dotenv())

# get APP_SECRET_KEY from .env file
APP_SECRET_KEY = env.get("APP_SECRET_KEY")

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.secret_key = APP_SECRET_KEY

    # Initialize Flask extensions here

    # Register blueprints here
    with app.app_context():
        from app.main import main
        app.register_blueprint(main, url_prefix='/')

        from app.auth import auth
        app.register_blueprint(auth, url_prefix='/auth')

    return app