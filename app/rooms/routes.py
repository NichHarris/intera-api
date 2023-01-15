from app.rooms import rooms
from app.rooms import controller as rooms_api
from app.transcripts import controller as transcripts_api
import app.auth.controller as auth

from os import environ as env
from dotenv import find_dotenv, load_dotenv
from config import Config

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
CORS(rooms, resources={r"/*": {"origins": "*"}})

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

    res = jsonify(message=message, data=rooms, status=200)

    res.headers.add('Access-Control-Allow-Origin', '*')
    return res

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

    users_list = room['users']
    status, message, transcript = transcripts_api.get_all_messages_by_room(room_id, users_list[0])

    if status == 0:
        # error occured
        return jsonify(error=message, status=401)

    # update messages array
    status, message = rooms_api.add_room_messages(room_id, transcript)

    if status == 0:
        # error occured
        return jsonify(error=message, status=401)

    return jsonify(message=message, data={'room_id': room_id}, status=200)


#####################
# SocketIO Handlers #
#####################

# TODO Handle returns

NAMESPACE = '/rooms'

# app = create_app()
# from app import socket_io
# from app import app

# socket_io = socketio.SocketIO(app, cors_allowed_origins="*")
# socket_io.run(app)

# @socket_io.on('connect', namespace=NAMESPACE)
# def connect():
#     print('Client connected')


# @socket_io.on('disconnect', namespace=NAMESPACE)
# def disconnect():
#     print('Client disconnected')


# @socket_io.on('create_room', namespace=NAMESPACE)
# def create_room(data):
#     pass


# @socket_io.on('join_room', namespace=NAMESPACE)
# def join_room(data):
#     room_id = data['room_id']
#     user_id = data['user_id']
#     join_room(room_id)


# @socket_io.on('leave_room', namespace=NAMESPACE)
# def leave_room(data):
#     room_id = data['room_id']
#     user_id = data['user_id']
    
#     users = rooms_api.get_room_users(room_id)

#     if users == None:
#         return

#     # check if user is host
#     if user_id == users[0]:
#         # close room
#         socketio.close_room(room_id, namespace=NAMESPACE)

#         for user in users:
#             socketio.disconnect(user, namespace=NAMESPACE)
#     else:
#         socketio.leave_room(user_id, room_id, namespace=NAMESPACE)
#         socketio.disconnect(user_id, namespace=NAMESPACE)


# @socket_io.on('send_message', namespace=NAMESPACE)
# def send_message(data):
#     room_id = data['room_id']
#     user_id = data['user_id']
#     message = data['message']


