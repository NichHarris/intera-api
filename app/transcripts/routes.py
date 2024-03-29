# API
from app.transcripts import transcripts
from app.transcripts import controller as transcripts_api
import app.auth.controller as auth

# Environment variables
from os import environ as env
from dotenv import find_dotenv, load_dotenv
from config import Config

# Flask
from flask_cors import CORS, cross_origin
from flask import request, jsonify

# load the environment variables from the .env file
load_dotenv(find_dotenv())
CORS(transcripts, resources={r"/*": {"origins": f'{Config.BASE_URL}/*'}})


@transcripts.post('/create_message')
@cross_origin(headers=["Origin", "Content-Type", "Authorization", "Accept"], supports_credentials=True)
@auth.requires_auth
def create_message():
    body = request.get_json(silent=True)
    if body is None:
        return jsonify(error='No body provided', status=400)

    room_id = body.get('room_id')
    to_user = body.get('to_user')
    text = body.get('message')
    type = body.get('type')

    # todo can clean up and make method to append all errors
    if room_id is None:
        return jsonify(error='Room ID not provided', status=400)
    if to_user is None:
        return jsonify(error='To User not provided', status=400)
    if text is None:
        return jsonify(error='Message not provided', status=400)
    if type is None:
        return jsonify(error='Message type not provided', status=400)

    # get user id from token
    token = auth.get_auth_token(request)
    user_info = auth.decode_jwt(token)
    user_id = user_info['nickname']

    status, message = transcripts_api.create_message_entry(room_id, to_user, user_id, text, message_type=type)

    if status == 0:
        return jsonify(error=message, status=401)
    else:
        return jsonify(message=message, status=200)


@transcripts.put('/edit_message')
@cross_origin(headers=["Origin", "Content-Type", "Authorization", "Accept"], supports_credentials=True)
@auth.requires_auth
def edit_message():
    body = request.get_json(silent=True)
    if body is None:
        return jsonify(error='No body provided', status=400)

    room_id = body.get('room_id')
    message = body.get('message')
    message_id = body.get('message_id')

    # todo can clean up and make method to append all errors
    if room_id is None:
        return jsonify(error='Room ID not provided', status=400)
    if message is None:
        return jsonify(error='Message not provided', status=400)
    if message_id is None:
        return jsonify(error='Message ID not provided', status=400)

    # get user id from token
    token = auth.get_auth_token(request)
    user_info = auth.decode_jwt(token)
    user_id = user_info['nickname']

    status, message = transcripts_api.edit_message_entry(room_id, user_id, message, message_id)

    if status == 0:
        return jsonify(error=message, status=401)
    else:
        return jsonify(message=message, status=200)


@transcripts.get('/get_message')
@cross_origin(headers=["Origin", "Content-Type", "Authorization", "Accept"], supports_credentials=True)
@auth.requires_auth
def get_message():
    room_id = request.args.get('room_id')

    # get user id from token
    token = auth.get_auth_token(request)
    user_info = auth.decode_jwt(token)
    user_id = user_info['nickname']

    status, message, data = transcripts_api.get_last_message(room_id, user_id)

    if status == 0:
        return jsonify(error=message, status=401)

    return jsonify(message=message, data=data, status=200)


@transcripts.get('/get_messages')
@cross_origin(headers=["Origin", "Content-Type", "Authorization", "Accept"], supports_credentials=True)
@auth.requires_auth
def get_messages():
    room_id = request.args.get('room_id')

    status, message, data = transcripts_api.get_all_messages_by_room(room_id)

    if status == 0:
        return jsonify(error=message, status=401)

    print(data)
    return jsonify(message=message, data=data, status=200)

# TODO Add route for setting if message is correct or not
