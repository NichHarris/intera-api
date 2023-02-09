from app.rooms import rooms
from app.rooms import controller as rooms_api
from app.transcripts import controller as transcripts_api
import app.auth.controller as auth
from app import mail
from os import environ as env
from dotenv import find_dotenv, load_dotenv
from config import Config, parse_json
import smtplib, ssl

from flask_cors import CORS, cross_origin
from flask import render_template, session, redirect, url_for, request, jsonify, Response
# from flask_socketio import SocketIO, emit, join_room, namespace, leave_room, send, disconnect
import flask_socketio as socketio
# import socketIO_client as socketio

from auth0.v3.authentication import Users, GetToken, base
from authlib.integrations.flask_oauth2 import ResourceProtector

from sendgrid import SendGridAPIClient
from flask_mail import Message

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

    invite_link = f'{Config.CLIENT_URL}/call-page/{room_id}'

    res = {
        'room_id': room_id,
        'invite_link': invite_link
    }

    return jsonify(message='success', data=res, status=200)


@rooms.post('/email_invite')
@cross_origin(headers=["Origin", "Content-Type", "Authorization", "Accept"], supports_credentials=True)
@auth.requires_auth
def email_invite():

    body = request.get_json(silent=True)
    if body is None:
        return jsonify(error='No body provided', status=400)

    room_id = body.get('room_id')
    to_email = body.get('email')
    
    if room_id is None:
        return jsonify(error='Room ID not provided', status=400)
    if to_email is None:
        return jsonify(error='Email not provided', status=400)

    token = auth.get_auth_token(request)
    user_info = auth.decode_jwt(token)

    from_email = user_info['email']
    user_id = user_info['nickname']

    if to_email:
        invite_link = f'{Config.CLIENT_URL}/call-page/{room_id}'

        try:
            msg = Message(subject='You have been invited to a room! - Intera',
                            sender=Config.MAIL_USERNAME,
                            recipients=[to_email],
                            body=f'You have been invited to a room!\n\nUser {user_id} wants you to join their meeting room!\n\nPlease join via this link: {invite_link}\n\nAlternatively, access via this link: {Config.CLIENT_URL} and join using the room code: {room_id} \n\nThank you for using Intera!')

            with smtplib.SMTP(Config.MAIL_SERVER, Config.MAIL_PORT) as server:
                server.starttls(context=ssl.create_default_context())
                server.login(Config.MAIL_USERNAME, Config.MAIL_PASSWORD)
                server.sendmail(Config.MAIL_USERNAME, to_email, str(msg))

        except Exception as e:
            return jsonify(error=f'Email not sent to {to_email} because\n {e}', status=400)
    else:
        return jsonify(error='Email not provided', status=403)

    return jsonify(message='success', data={'room_id': room_id, 'email_id': 0}, status=200)


@rooms.post('/register_room')
@cross_origin(headers=["Origin", "Content-Type", "Authorization", "Accept"], supports_credentials=True)
@auth.requires_auth
def register_room():
    body = request.get_json(silent=True)
    if body is None:
        return jsonify(error='No body provided', status=400)

    room_id = body.get('room_id')
    host_type = body.get('host_type')
    
    if room_id is None:
        return jsonify(error='Room ID not provided', status=400)
    if host_type is None:
        return jsonify(error='Host type not provided', status=400)

    # get user id from token
    token = auth.get_auth_token(request)
    user_info = auth.decode_jwt(token)
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
    body = request.get_json(silent=True)
    if body is None:
        return jsonify(error='No body provided', status=400)

    room_id = body.get('room_id')

    if room_id is None:
        return jsonify(error='Room ID not provided', status=400)

    # get user id from token
    token = auth.get_auth_token(request)
    user_info = auth.decode_jwt(token)
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

    if room_id is None:
        return jsonify(error='Room ID not provided', status=400)

    # get room
    status, message, room = rooms_api.get_room(room_id)
    
    if status == 0:
        # error occured
        return jsonify(error=message, status=404)

    return jsonify(message=message, data=parse_json(room.next()), status=200)


@rooms.get('/get_all_rooms_by_user')
@cross_origin(headers=["Origin", "Content-Type", "Authorization", "Accept"], supports_credentials=True)
@auth.requires_auth
def get_all_rooms_by_user():
    # get user id from token
    token = auth.get_auth_token(request)
    user_info = auth.decode_jwt(token)
    user_id = user_info['nickname']

    if user_id is None:
        return jsonify(error='User ID unrecognized', status=401)

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
    body = request.get_json(silent=True)
    if body is None:
        return jsonify(error='No body provided', status=400)

    room_id = body.get('room_id')

    if room_id is None:
        return jsonify(error='Room ID not provided', status=400)

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
    body = request.get_json(silent=True)
    if body is None:
        return jsonify(error='No body provided', status=400)

    room_id = body.get('room_id')

    if room_id is None:
        return jsonify(error='Room ID not provided', status=400)

    status, message, transcript = transcripts_api.get_all_messages_by_room(room_id)

    if status == 0:
        # error occured
        return jsonify(error=message, status=404)

    # update messages array
    status, message = rooms_api.add_room_messages(room_id, transcript)

    if status == 0:
        # error occured
        return jsonify(error=message, status=401)

    return jsonify(message=message, data={'room_id': room_id}, status=200)
