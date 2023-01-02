from app.practice_module import practice_module
from app.practice_module import controller as practice_api
from app.auth import auth

from os import environ as env
from dotenv import find_dotenv, load_dotenv
from config import Config

from flask_cors import CORS
from flask import render_template, session, redirect, url_for, request, jsonify, Response

from auth0.v3.authentication import Users, GetToken
from authlib.integrations.flask_oauth2 import ResourceProtector

# load the environment variables from the .env file
load_dotenv(find_dotenv())
CORS(practice_module, resources={r"/*": {"origins": "*"}})


@practice_module.get('/get_word')
def get_word():
    status, message, word = practice_api.retrieve_random_word()

    if status == 0:
        return jsonify(error=message, status=401)
    else:
        return jsonify(message=message, data=word, status=200)

@practice_module.post('/create_word')
def create_word():
    word = request.args.get('word')
    url = request.args.get('url')

    status, message = practice_api.create_word_entry(word, url)

    if status == 0:
        return jsonify(error=message, status=401)
    else:
        return jsonify(message=message, status=200)


@practice_module.put('/get_word_url')
def get_word_url():
    word = request.args.get('word')

    status, message, url = practice_api.get_word_video_url(word)

    if status == 0:
        return jsonify(error=message, status=401)
    else:
        return jsonify(message=message, data=url, status=200)


@practice_module.put('/delete_word')
def delete_word():
    word = request.args.get('word')

    status, message = practice_api.delete_word(word)

    if status == 0:
        return jsonify(error=message, status=401)
    else:
        return jsonify(message=message, status=200)


@practice_module.put('/update_word_classification')
def update_word_classification():
    word = request.args.get('word')
    classification = request.args.get('classification')

    status, message = practice_api.set_classified_status(word, classification)

    if status == 0:
        return jsonify(error=message, status=401)
    else:
        return jsonify(message=message, status=200)
