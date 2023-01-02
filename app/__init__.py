from os import environ as env
from dotenv import find_dotenv, load_dotenv
from flask import Flask
from config import Config
from flask_cors import CORS
from flask_mail import Mail

# load .env file
load_dotenv(find_dotenv())
mail = Mail()

# get APP_SECRET_KEY from .env file
APP_SECRET_KEY = env.get("APP_SECRET_KEY")
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.secret_key = APP_SECRET_KEY
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    mail = Mail(app)
    # Initialize Flask extensions here

    # Register blueprints here
    with app.app_context():
        from app.rooms import rooms
        app.register_blueprint(rooms, url_prefix='/api/rooms')

        from app.auth import auth
        app.register_blueprint(auth, url_prefix='/api/auth')

        from app.practice_module import practice_module
        app.register_blueprint(practice_module, url_prefix='/api/practice')

    return app