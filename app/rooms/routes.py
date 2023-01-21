from app.rooms import rooms
from app.rooms import controller as rooms_api
from app.transcripts import controller as transcripts_api
import app.auth.controller as auth

from os import environ as env
from dotenv import find_dotenv, load_dotenv
from config import Config, parse_json

from flask_cors import CORS, cross_origin
from flask import render_template, session, redirect, url_for, request, jsonify, Response
# from flask_socketio import SocketIO, emit, join_room, namespace, leave_room, send, disconnect
import flask_socketio as socketio
# import socketIO_client as socketio

from auth0.v3.authentication import Users, GetToken, base
from authlib.integrations.flask_oauth2 import ResourceProtector

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import *

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

# load the environment variables from the .env file
load_dotenv(find_dotenv())
CORS(rooms, resources={r"/*": {"origins": f'{Config.BASE_URL}/*'}})


@rooms.get('/create_room_id')
@cross_origin(headers=["Origin", "Content-Type", "Authorization", "Accept"], supports_credentials=True)
@auth.requires_auth
def create_room_id():
    room_id = rooms_api.generate_room_id()
    token = auth.get_auth_token(request)
    user_info = auth.decode_jwt(token)
    print(user_info)

    invite_link = f'{Config.BASE_URL}/room/{room_id}'

    res = {
        'room_id': room_id,
        'invite_link': invite_link
    }

    return jsonify(message='success', data=res, status=200)


@rooms.post('/email_invite')
@cross_origin(headers=["Origin", "Content-Type", "Authorization", "Accept"], supports_credentials=True)
@auth.requires_auth
def email_invite():
    room_id = request.args.get('room_id')
    to_email = request.args.get('email')
    
    token = auth.get_auth_token(request)
    user_info = auth.decode_jwt(token)

    from_email = user_info['email']

    if email:

        # TODO: Format
        invite_link = f'{Config.BASE_URL}/room/{room_id}'
        message = Mail(from_email=From(from_email, 'Example From Name'),
            to_emails=To(to_email, 'Example To Name'),
            subject=Subject('Sending with SendGrid is Fun'),
            plain_text_content=PlainTextContent(f'Invite link: {invite_link}'),
            html_content=HtmlContent(f'<strong>and easy to do anywhere, even {invite_link}</strong>'))

        sendgrid_api = SendGridAPIClient(env.get('SENDGRID_API_KEY'))
        response = sendgrid_api.send(message)

        print(response.status_code)
        print(response.body)
        print(response.headers)
    else:
        return jsonify(error='Email not provided', status=401)

    return jsonify(message='success', data={'room_id': room_id, 'email_id': 0}, status=200)


@rooms.post('/register_room')
@cross_origin(headers=["Origin", "Content-Type", "Authorization", "Accept"], supports_credentials=True)
@auth.requires_auth
def register_room():
    room_id = request.args.get('room_id')
    host_type = request.args.get('host_type')
    user_info = auth.decode_jwt(auth.get_auth_token(request))
    user_id = user_info['nickname']

    # # validate room doesn't exist
    # status, message = rooms_api.validate_room(room_id, user_id)

    # if status != 0:
    #     # error occured
    #     return jsonify(error=message, status=401)

    status, message = rooms_api.create_room(room_id, user_id, host_type)

    if status != 1:
        # error occured
        return jsonify(error=message, status=401)

    return jsonify(message=message, data={'room_id': room_id}, status=200)


# create route for joining room
@rooms.put('/join_room')
@cross_origin(headers=["Origin", "Content-Type", "Authorization", "Accept"], supports_credentials=True)
@auth.requires_auth
def join_room():
    room_id = request.args.get('room_id')
    user_info = auth.decode_jwt(auth.get_auth_token(request))
    user_id = user_info['nickname']

    # check if room is valid
    status, message = rooms_api.validate_room(room_id, user_id)

    if status == 0:
        # error occured
        return jsonify(error=message, status=401)

    # register user in room
    status, message = rooms_api.register_user_in_room(room_id, user_id)
    
    if status == 0:
        # error occured
        return jsonify(error=message, status=401)

    return jsonify(message=message, data={'room_id': room_id}, status=200)


@rooms.get('/get_room_info')
@cross_origin(headers=["Origin", "Content-Type", "Authorization", "Accept"], supports_credentials=True)
@auth.requires_auth
def get_room_info():
    room_id = request.args.get('room_id')

    # # check if room is valid
    # status, message = rooms_api.validate_room(room_id)

    # if status == 0:
    #     # error occured
    #     return jsonify(error=message, status=401)

    # get room
    status, message, room = rooms_api.get_room(room_id)
    
    if status == 0:
        # error occured
        return jsonify(error=message, status=401)

    return jsonify(message=message, data=room, status=200)


@rooms.get('/get_all_rooms_by_user')
@cross_origin(headers=["Origin", "Content-Type", "Authorization", "Accept"], supports_credentials=True)
@auth.requires_auth
def get_all_rooms_by_user():
    user_id = request.args.get('user_id')

    user_info = auth.decode_jwt(auth.get_auth_token(request))
    user_nickname = user_info['nickname']

    if user_id != user_nickname:
        return jsonify(error='Unauthorized', status=401)

    # get all rooms
    status, message, rooms = rooms_api.get_all_rooms_by_user(user_id)
    
    if status == 0:
        # error occured
        return jsonify(error=message, status=401)

    return jsonify(message=message, data=parse_json(rooms), status=200)

@rooms.put('/close_room')
@cross_origin(headers=["Origin", "Content-Type", "Authorization", "Accept"], supports_credentials=True)
@auth.requires_auth
def close_room():
    room_id = request.args.get('room_id')

    # update room status
    status, message = rooms_api.update_room_status(room_id, False)
    
    if status == 0:
        # error occured
        return jsonify(error=message, status=401)

    return jsonify(message=message, data={'room_id': room_id}, status=200)


@rooms.put('/add_messages')
@cross_origin(headers=["Origin", "Content-Type", "Authorization", "Accept"], supports_credentials=True)
@auth.requires_auth
def add_messages():
    room_id = request.args.get('room_id')

    # check if room is active 
    # status, message = rooms_api.validate_room(room_id)

    # if status == 0:
    #     # error occured
    #     return jsonify(error=message, status=401)

    status, message, room = rooms_api.get_room(room_id)

    if status == 0:
        # error occured
        return jsonify(error=message, status=401)

    status, message, transcript = transcripts_api.get_all_messages_by_room(room_id)

    if status == 0:
        # error occured
        return jsonify(error=message, status=401)

    # update messages array
    status, message = rooms_api.add_room_messages(room_id, transcript)

    if status == 0:
        # error occured
        return jsonify(error=message, status=401)

    return jsonify(message=message, data={'room_id': room_id}, status=200)
