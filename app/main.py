# from os import environ as env
# from dotenv import find_dotenv, load_dotenv
# from config import Config

# from flask import Flask
# from flask_socketio import SocketIO
# from flask_cors import CORS
# from app.rooms import rooms
# from app.practice_module import practice_module
# from app.transcripts import transcripts
# from app.auth import auth

# # load .env file
# load_dotenv(find_dotenv())


# from app import s_webrtc, app
# # get APP_SECRET_KEY from .env file
# APP_SECRET_KEY = env.get("APP_SECRET_KEY")

# app = Flask(__name__)
# app.config.from_object(Config)
# app.secret_key = APP_SECRET_KEY

# CORS(app, resources={r"/api/*": {"origins": "*"}})
# app.register_blueprint(rooms, url_prefix='/api/rooms')
# app.register_blueprint(practice_module, url_prefix='/api/practice')
# app.register_blueprint(transcripts, url_prefix='/api/transcripts')
# app.register_blueprint(auth, url_prefix='/api/auth')

# socketio = SocketIO(app, cors_allowed_origins="*")

# if __name__ == '__main__':
#     # socket_io.run(app, host='127.0.0.1', port=5000)
#     print('HELLO WORLD')
#     try:
#         print('starting ---------------------------------------------------------------------- ')
#         s_webrtc.run(app, host="localhost", port=9000)
        
#         print(s_webrtc)
#     except:
#         print("An exception occurred")
#     print("started ---------------------------------------------------------------------- ")