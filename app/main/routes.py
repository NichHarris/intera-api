from app.main import main
from app.auth import auth
from app.rooms import rooms
from os import environ as env
from dotenv import find_dotenv, load_dotenv
import json


from flask_cors import CORS

import app.rooms.controller as rooms_api
from app.rooms.controller import (
    generate_room_id,
    create_room,
    validate_room,
    register_user_in_room,
    get_room,
    update_room_status,
    add_room_messages,
    get_all_rooms_by_id,
)

from auth0.v3.authentication import Users, GetToken
from authlib.integrations.flask_oauth2 import ResourceProtector
from flask import render_template, session, redirect, url_for, request, jsonify, Response
from config import Config
from flask_mail import Mail, Message
# from sengrid import SendGridAPIClient

from app import create_app

app = create_app()
mail = Mail(app)

# load the environment variables from the .env file
load_dotenv(find_dotenv())

AUTH0_CLIENT_SECRET = env.get("AUTH0_CLIENT_SECRET")

CORS(main, resources={r"/*": {"origins": "*"}})

@main.route('/')
def index():
    if session:
        return render_template('home.html')
    else:
        # redirect to login
        # TODO use next js to fetch
        return redirect(url_for('auth.login'))

@main.get('/create_room_id')
def create_room_id():
    room_id = generate_room_id()

    invite_link = f'{Config.BASE_URL}/api/rooms/join_room?room_id={room_id}'

    res = {
        'room_id': room_id,
        'invite_link': invite_link
    }

    return jsonify(message='success', data=res, status=200)

@main.post('/email_invite')
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
    else:
        return jsonify(error='Email not provided', status=401)

    mail.send(msg)
    return jsonify(message='success', data={'room_id': room_id, 'email_id': 0}, status=200)

@main.post('/register_room')
def register_room():
    room_id = request.args.get('room_id')
    # user_id = request.form.get('user_id')
    user_id = 'test'
    host_type = request.args.get('host_type')

    # validate room doesn't exist
    status, message = validate_room(room_id, user_id)

    if status != 0:
        # error occured
        return jsonify(error=message, status=401)

    status, message = create_room(room_id, user_id, host_type)

    if status != 1:
        # error occured
        return jsonify(error=message, status=401)

    return jsonify(message=message, data={'room_id': room_id}, status=200)

# create route for joining room
@main.get('/join_room')
def join_room():
    room_id = request.args.get('room_id')
    user_id = request.form.get('user_id')

    # check if room is valid
    status, message = validate_room(room_id)

    if status == 0:
        # error occured
        return jsonify(error=message, status=401)

    # register user in room
    status, message = register_user_in_room(room_id, user_id)
    
    if status == 0:
        # error occured
        return jsonify(error=message, status=401)

    return jsonify(message=message, data={'room_id': room_id}, status=200)

@main.get('/get_room_info')
def get_room_info():
    room_id = request.args.get('room_id')

    # check if room is valid
    status, message = validate_room(room_id)

    if status == 0:
        # error occured
        return jsonify(error=message, status=401)

    # get room
    status, message, room = get_room(room_id)
    
    if status == 0:
        # error occured
        return jsonify(error=message, status=401)

    return jsonify(message=message, data=room, status=200)

@main.get('/get_all_rooms_by_id')
def get_all_rooms_by_id():
    user_id = request.args.get('user_id')
    # user_id = 'test'

    # get all rooms
    status, message, rooms = rooms_api.get_all_rooms_by_id(user_id)
    
    if status == 0:
        # error occured
        return jsonify(error=message, status=401)
    print(rooms)
    # return jsonify(message=message, data=, status=200)
    return Response(json.dumps(rooms, default=str), mimetype='application/json')

@main.put('/close_room')
def close_room():
    room_id = request.args.get('room_id')

    # update room status
    status, message = update_room_status(room_id, False)
    
    if status == 0:
        # error occured
        return jsonify(error=message, status=401)

    return jsonify(message=message, data={'room_id': room_id}, status=200)

@main.put('/add_messages')
def add_messages():
    room_id = request.args.get('room_id')
    # messages = request.args.get('messages')
    messages = []
    # todo: fetch all messages from the messages table relating to room_id
    # check if room is valid
    status, message = validate_room(room_id)

    if status == 0:
        # error occured
        return jsonify(error=message, status=401)

    # update room status
    status, message = add_room_messages(room_id, messages)
    
    if status == 0:
        # error occured
        return jsonify(error=message, status=401)

    return jsonify(message=message, data={'room_id': room_id}, status=200)
