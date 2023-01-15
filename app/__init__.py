from os import environ as env
from dotenv import find_dotenv, load_dotenv
from flask import Flask
from config import Config
from flask_cors import CORS
import flask_socketio as socketio

# load .env file
load_dotenv(find_dotenv())

# get APP_SECRET_KEY from .env file
APP_SECRET_KEY = env.get("APP_SECRET_KEY")
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.secret_key = APP_SECRET_KEY
    # TODO: Include cloud target URL in origins field once project is hosted remotely
    CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

    socket_io = socketio.SocketIO(app, cors_allowed_origins="*")
    # socket_io.run(app)

    # Register blueprints here
    with app.app_context():
        from app.rooms import rooms
        app.register_blueprint(rooms, url_prefix='/api/rooms')

        from app.transcripts import transcripts
        app.register_blueprint(transcripts, url_prefix='/api/transcripts')
        
        from app.auth import auth
        app.register_blueprint(auth, url_prefix='/api/auth')

        from app.practice_module import practice_module
        app.register_blueprint(practice_module, url_prefix='/api/practice')

        from app.neural_net import neural_net
        app.register_blueprint(neural_net, url_prefix='/api/neural_net')

    return app
