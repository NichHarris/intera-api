from os import environ as env
from dotenv import find_dotenv, load_dotenv
from flask import Flask
from flask_mail import Mail, Message
from config import Config
import flask_socketio as socketio

from flask_cors import CORS

# load .env file
load_dotenv(find_dotenv())

APP_SECRET_KEY = env.get("APP_SECRET_KEY")
# def create_app():
app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = APP_SECRET_KEY

app.config['MAIL_SERVER'] = Config.MAIL_SERVER
app.config['MAIL_PORT'] = Config.MAIL_PORT
app.config['MAIL_USERNAME'] = Config.MAIL_USERNAME
app.config['MAIL_PASSWORD'] = Config.MAIL_PASSWORD
app.config['MAIL_USE_TLS'] = Config.MAIL_USE_TLS
app.config['MAIL_USE_SSL'] = Config.MAIL_USE_SSL

CORS(app, resources={r"/api/*": {"origins": [f'{Config.BASE_URL}/*', {'http://localhost:3000'}] }})

socket_io = socketio.SocketIO(app, cors_allowed_origins=[f'{Config.CLIENT_URL}'])
mail = Mail(app)

# Register blueprints here
from app.rooms import rooms
app.register_blueprint(rooms, url_prefix='/api/rooms')

from app.transcripts import transcripts
app.register_blueprint(transcripts, url_prefix='/api/transcripts')

from app.practice_module import practice_module
app.register_blueprint(practice_module, url_prefix='/api/practice')

from app.neural_net import neural_net
app.register_blueprint(neural_net, url_prefix='/api/neural_net')

from app.auth import auth
app.register_blueprint(auth, url_prefix='/api/auth')

from app.sockets import sockets
app.register_blueprint(sockets)
