from app.rooms import rooms
from app.rooms import controller as rooms_api
from app.transcripts import controller as transcripts_api
from app.auth import auth
import app

from os import environ as env
from dotenv import find_dotenv, load_dotenv
from config import Config

from flask_cors import CORS
from flask import render_template, session, redirect, url_for, request, jsonify, Response
from flask_mail import Message

from auth0.v3.authentication import Users, GetToken
from authlib.integrations.flask_oauth2 import ResourceProtector

# load the environment variables from the .env file
load_dotenv(find_dotenv())
mail = app.mail
CORS(rooms, resources={r"/*": {"origins": "*"}})


# TODO Remove this
@rooms.route('/')
def index():
    if session:
        return render_template('home.html')
    else:
        return render_template('home.html')
        # redirect to login
        # TODO use next js to fetch
        # return redirect(url_for('auth.login'))


@rooms.get('/create_room_id')
def create_room_id():
    room_id = rooms_api.generate_room_id()

    invite_link = f'{Config.BASE_URL}/api/rooms/join_room?room_id={room_id}'

    res = {
        'room_id': room_id,
        'invite_link': invite_link
    }

    return jsonify(message='success', data=res, status=200)


@rooms.post('/email_invite')
def email_invite():
    room_id = request.args.get('room_id')
    email = request.args.get('email')
    # user_id = request.form.get('user_id')
    user_id = 'test'

    # message = sendgrid.Mail()
    msg = None
    if email:
        msg = Message('Twilio SendGrid Test Email', recipients=['harris.nicholas1998@gmail.com'], sender='harris.nicholas1998@gmail.com')
        msg.body = 'This is a test email!'
        msg.html = '<p>This is a test email!</p>'
        mail.send(msg)
    else:
        return jsonify(error='Email not provided', status=401)

    return jsonify(message='success', data={'room_id': room_id, 'email_id': 0}, status=200)


@rooms.post('/register_room')
def register_room():
    room_id = request.args.get('room_id')
    # user_id = request.form.get('user_id')
    user_id = 'test'
    host_type = request.args.get('host_type')

    # validate room doesn't exist
    status, message = rooms_api.validate_room(room_id, user_id)

    if status != 0:
        # error occured
        return jsonify(error=message, status=401)

    status, message = rooms_api.create_room(room_id, user_id, host_type)

    if status != 1:
        # error occured
        return jsonify(error=message, status=401)

    return jsonify(message=message, data={'room_id': room_id}, status=200)


# create route for joining room
@rooms.put('/join_room')
def join_room():
    room_id = request.args.get('room_id')
    # user_id = request.form.get('user_id')
    user_id = request.args.get('user_id')

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


@rooms.get('/get_all_rooms_by_id')
def get_all_rooms_by_id():
    user_id = request.args.get('user_id')
    # user_id = 'test'

    # get all rooms
    status, message, rooms = rooms_api.get_all_rooms_by_id(user_id)
    
    if status == 0:
        # error occured
        return jsonify(error=message, status=401)

    return jsonify(message=message, data=rooms, status=200)


@rooms.put('/close_room')
def close_room():
    room_id = request.args.get('room_id')

    # update room status
    status, message = rooms_api.update_room_status(room_id, False)
    
    if status == 0:
        # error occured
        return jsonify(error=message, status=401)

    return jsonify(message=message, data={'room_id': room_id}, status=200)


@rooms.put('/add_messages')
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
