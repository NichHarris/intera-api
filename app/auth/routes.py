from os import environ as env
from dotenv import find_dotenv, load_dotenv
from urllib.parse import quote_plus, urlencode
from authlib.integrations.flask_client import OAuth
from auth0.v3.authentication import Users, GetToken
from flask import Flask, redirect, render_template, session, url_for, request, jsonify

from authlib.integrations.flask_oauth2 import ResourceProtector
