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

