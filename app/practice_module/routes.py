from app.practice_module import practice_module
import app.practice_module.controller as controller
from os import environ as env
from auth0.v3.authentication import Users, GetToken
from authlib.integrations.flask_oauth2 import ResourceProtector
from flask import render_template, session, redirect, url_for
from config import Config

AUTH0_CLIENT_SECRET = env.get("AUTH0_CLIENT_SECRET")

