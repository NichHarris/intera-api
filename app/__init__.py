import json
from os import environ as env
from urllib.parse import quote_plus, urlencode

from authlib.integrations.flask_client import OAuth
from dotenv import find_dotenv, load_dotenv
from flask import Flask, redirect, render_template, session, url_for
from config import Config

# ENV_FILE = find_dotenv()
# if ENV_FILE:
#     load_dotenv(ENV_FILE)

# # create the flask object
# app = Flask(__name__)
# app.secret_key = env.get("APP_SECRET_KEY")

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.secret_key = config_class.APP_SECRET_KEY
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

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=env.get("PORT", 3005))
#     print("Hello World")