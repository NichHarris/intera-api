from app.practice_module import practice_module
from app.practice_module import controller as practice_api
import app.auth.controller as auth

from os import environ as env
from dotenv import find_dotenv, load_dotenv
from config import Config

from flask_cors import CORS, cross_origin
from flask import render_template, session, redirect, url_for, request, jsonify, Response

from auth0.v3.authentication import Users, GetToken
from authlib.integrations.flask_oauth2 import ResourceProtector

# load the environment variables from the .env file
load_dotenv(find_dotenv())
CORS(practice_module, resources={r"/*": {"origins": "*"}})


@practice_module.get('/get_word')
@cross_origin(headers=["Origin", "Content-Type", "Authorization", "Accept"], supports_credentials=True)
@auth.requires_auth
def get_word():
    status, message, word = practice_api.retrieve_random_word()

    if status == 0:
        return jsonify(error=message, status=401)
    else:
        return jsonify(message=message, data=word, status=200)

@practice_module.post('/create_word')
@cross_origin(headers=["Origin", "Content-Type", "Authorization", "Accept"], supports_credentials=True)
@auth.requires_auth
def create_word():
    word = request.args.get('word')
    url = request.args.get('url')

    status, message = practice_api.create_word_entry(word, url)

    if status == 0:
        return jsonify(error=message, status=401)
    else:
        return jsonify(message=message, status=200)


@practice_module.get('/get_word_url')
@cross_origin(headers=["Origin", "Content-Type", "Authorization", "Accept"], supports_credentials=True)
@auth.requires_auth
def get_word_url():
    word = request.args.get('word')

    status, message, url = practice_api.get_word_video_url(word)

    if status == 0:
        return jsonify(error=message, status=401)
    else:
        return jsonify(message=message, data=url, status=200)


@practice_module.delete('/delete_word')
@cross_origin(headers=["Origin", "Content-Type", "Authorization", "Accept"], supports_credentials=True)
@auth.requires_auth
def delete_word():
    word = request.args.get('word')

    status, message = practice_api.delete_word(word)

    if status == 0:
        return jsonify(error=message, status=401)
    else:
        return jsonify(message=message, status=200)


@practice_module.put('/update_word_classification')
@cross_origin(headers=["Origin", "Content-Type", "Authorization", "Accept"], supports_credentials=True)
@auth.requires_auth
def update_word_classification():
    word = request.args.get('word')
    classification = request.args.get('classification')

    status, message = practice_api.set_classified_status(word, classification)

    if status == 0:
        return jsonify(error=message, status=401)
    else:
        return jsonify(message=message, status=200)


#####################
# SocketIO Handlers #
#####################

# from flask_socketio import SocketIO, emit, join_room, namespace
# from app import create_app

# # Not sure about this
# socket_io = SocketIO(create_app())

# NAMESPACE = '/practice_module'

# @socket_io.on('start_recording', namespace=NAMESPACE)
# def start_recording(data):
#     room_id = data['room_id']
#     user_id = data['user_id']

# @socket_io.on('stop_recording', namespace=NAMESPACE)
# def stop_recording(data):
#     room_id = data['room_id']
#     user_id = data['user_id']