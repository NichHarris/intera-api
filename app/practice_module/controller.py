from config import Database
from pymongo import errors

from os import environ as env
from dotenv import find_dotenv, load_dotenv

from datetime import datetime
import random

# load the environment variables from the .env file
load_dotenv(find_dotenv())

# get a reference to the databases
intera_practice_db = Database.client.intera_practice_db

# get a reference to the collections
try: 
    word_data = intera_practice_db['word_data']
except errors.CollectionInvalid as err:
    print(err)

def create_word_entry(word, url):
    word_entry = {'word': word, 'url': url, 'date_created': datetime.now()}
    word_data.insert_one(word_entry)

def retrieve_random_word(self):

    # get random word from mongodb without using aggregate
    count = word_data.count_documents({})
    random_index = random.randint(0, count - 1)
    word = word_data.find()[random_index]

    return word

def get_word_video_url(word):
    word_entry = word_data.find_one({'word': word})

    if word_entry:
        return word_entry['url']
    
    return None