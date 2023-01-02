from app.transcripts import transcripts
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
CORS(transcripts, resources={r"/*": {"origins": "*"}})


@transcripts.post('/create_message')
def create_message():
    room_id = request.args.get('room_id')
    to_user = request.args.get('to_user')
    text = request.args.get('message')

    from_user = request.form.get('user_id')
    type = request.form.get('type')

    status, message = transcripts_api.create_message_entry(room_id, to_user, from_user, text, message_type=type)

    if status == 0:
        return jsonify(error=message, status=401)
    else:
        return jsonify(message=message, status=200)


@transcripts.put('/edit_message')
def edit_message():
    room_id = request.args.get('room_id')
    text = request.args.get('message')
    user_id = request.form.get('user_id')

    status, message = transcripts_api.edit_message_entry(room_id, user_id, text)

    if status == 0:
        return jsonify(error=message, status=401)
    else:
        return jsonify(message=message, status=200)


@transcripts.put('/get_message')
def get_message():
    room_id = request.args.get('room_id')
    user_id = request.form.get('user_id')

    status, message, data = transcripts_api.get_message(room_id, user_id)

    if status == 0:
        return jsonify(error=message, status=401)
    else:
        return jsonify(message=message, data=data, status=200)
