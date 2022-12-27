# import the MongoClient class
from pymongo import MongoClient
from os import environ as env
import os
from dotenv import find_dotenv, load_dotenv
import uuid
import random
from datetime import datetime
import certifi

# load the environment variables from the .env file
load_dotenv(find_dotenv())
basedir = os.path.abspath(os.path.dirname(__file__))

class DB(object):
    # create a MongoClient instance
    client = MongoClient(f"mongodb+srv://{env.get('USERNAME')}:{env.get('PASSWORD')}@asl-cluster.kixgnlo.mongodb.net/?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE", tlsCAFile=certifi.where())

    # get a reference to the databases
    intera_call_transcripts_db = client.intera_call_transcripts
    intera_calls_db = client.intera_calls
    intera_practice_db = client.intera_practice_db

    # get a reference to the collections
    users = intera_calls_db['users'] # may not be needed, we can use the auth0 users
    rooms = intera_calls_db['rooms']
    transcripts = intera_call_transcripts_db['transcripts']
    word_data = intera_practice_db['word_data']

    ###########################
    # Meetings DB #
    ###########################

    # TODO: Error handling
    # generate a random room_id using the uuid library
    def generate_room_id(self):
        random_id = str(uuid.uuid4())

        while self.rooms.find({'_id': random_id}).count() != 0:
            random_id = str(uuid.uuid4())

        return random_id

    def create_room(self, user_id):
        room_id = self.generate_room_id()

        room = {'_id': room_id, 'users': {user_id}}
        self.rooms.insert_one(room)
        return room_id

    def validate_room(self, room_id, user_id):
        room = self.rooms.find_one({'_id': room_id})

        if room is None:
            return False
        
        if len(room['users']) == 2:
            if user_id in room['users']:
                return True
            else:
                return False
        
        return True

    def register_user_in_room(self, room_id, user_id):
        room = self.rooms.find_one({'_id': room_id})

        if room is None:
            return False

        room_users = room['users']

        if len(room_users) == 2:
            return False
        else:
            if user_id in room_users:
                return False

            room_users.add(user_id)
            self.rooms.update_one({'_id': room_id}, {'$set': {'users': room_users}})
        
        return True

    ###########################
    # Transcripts DB #
    ###########################

    def create_transcript_entry(self, room_id, guest_id, host_id, text):
        transcript_id = f'{room_id}_{guest_id}_{host_id}_{datetime.now()}'
        transcript = {'_id': transcript_id, 'date_created': datetime.now(), 'room_id': room_id, 'guest_id': guest_id, 'host_id': host_id, 'text': text}
        self.transcripts.insert_one(transcript)

    def get_all_transcripts(self, user_id):
        all_transcripts = self.transcripts.find({'$or': [{'guest_id': user_id}, {'host_id': user_id}]}).sort('date_created', -1)

        return all_transcripts.pretty()

    def get_transcript(self, transcript_id):
        transcript = self.transcripts.find_one({'_id': transcript_id})

        if transcript is None:
            return None
        
        return transcript

    ###########################
    # Practice DB #
    ###########################

    def create_word_entry(self, word, url):
        word_entry = {'_id': word, 'url': url, 'date_created': datetime.now()}
        self.word_data.insert_one(word_entry)

    def retrieve_random_word(self):

        # get random word from mongodb without using aggregate
        count = self.word_data.count_documents({})
        random_index = random.randint(0, count - 1)
        word = self.word_data.find()[random_index]

        return word

    def get_word_video_url(self, word):
        word_entry = self.word_data.find_one({'_id': word})

        if word_entry:
            return word_entry['url']
        
        return None
