from pymongo import MongoClient
from pymongo import errors
from os import environ as env
from dotenv import find_dotenv, load_dotenv
from datetime import datetime
import certifi

# load the environment variables from the .env file
load_dotenv(find_dotenv())

client = MongoClient(f"mongodb+srv://{env.get('USERNAME')}:{env.get('PASSWORD')}@asl-cluster.kixgnlo.mongodb.net/?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE", tlsCAFile=certifi.where())

# get a reference to the databases
intera_calls_db = client.intera_calls
# get a reference to the collections
try: 
    transcripts = intera_calls_db['transcripts']
except errors.CollectionInvalid as err:
    print(err)

def create_transcript_entry(room_id, to_user, from_user, text):
    message_id = f'{room_id}_{from_user}_{to_user}_{datetime.now()}'
    transcript = {'_id': message_id, 'date_created': datetime.now(), 'room_id': room_id, 'to': to_user, 'from': from_user, 'text': text}
    transcripts.insert_one(transcript)

def get_all_transcripts(user_id):
    all_transcripts = transcripts.find({'$or': [{'guest_id': user_id}, {'host_id': user_id}]}).sort('date_created', -1)

    return all_transcripts.pretty()

def get_transcript(transcript_id):
    transcript = transcripts.find_one({'_id': transcript_id})

    if transcript is None:
        return None

    return transcript