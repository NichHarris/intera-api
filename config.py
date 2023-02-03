import os
from os import environ as env
from dotenv import find_dotenv, load_dotenv
from pymongo import MongoClient
import json
from bson import json_util

# load the environment variables from the .env file
load_dotenv(find_dotenv())

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    AUTH0_CLIENT_ID='YfFXlkN6VSJtKISCKRrUNUdqPDjp5oZb'
    AUTH0_DOMAIN='dev-gsbv87qpmgwdpjej.us.auth0.com'
    AUTH0_CALLBACK_URL='http://localhost:5000/auth/callback'
    BASE_URL= env.get('BASE_URL') or 'http://localhost:5000'
    CLIENT_URL= env.get('CLIENT_URL') or 'http://localhost:3000'
    MAIL_SERVER='smtp.sendgrid.net'
    MAIL_PORT=587
    MAIL_USE_TLS=True
    MAIL_USERNAME='apikey'
    MAIL_PASSWORD=env.get('SENDGRID_API_KEY')
    MAIL_DEFAULT_SENDER=env.get('MAIL_DEFAULT_SENDER')
class Database(object):
    client = MongoClient(f"mongodb+srv://{env.get('USERNAME')}:{env.get('PASSWORD')}@{env.get('DATABASE_URL')}")
    intera_calls_db = 'intera_calls'
    intera_practice_db = 'intera_practice_db'
    rooms_collection = 'rooms'
    messages_collection = 'messages'
    word_data_collection = 'word_data'
    attemted_words_collection = 'attemted_words'

def parse_json(data):
    return json.loads(json_util.dumps(data))