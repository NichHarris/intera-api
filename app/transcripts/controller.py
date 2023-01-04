from config import Database
from pymongo import errors, results

from os import environ as env
from dotenv import find_dotenv, load_dotenv
from datetime import datetime

# load the environment variables from the .env file
load_dotenv(find_dotenv())

# get a reference to the databases
intera_calls_db = Database.client[Database.intera_calls_db]

# get a reference to the collections
try: 
    messages = intera_calls_db[Database.messages_collection]
except errors.CollectionInvalid as err:
    print(err)


def create_message_entry(room_id, to_user, from_user, text, edited=False, message_type='ASL', correct=True):
    message = {'date_created': datetime.now(), 'room_id': room_id, 'to': to_user, 'from': from_user, 'text': text,\
        'edited': edited, 'message_type': message_type, 'correct': correct}

    result = messages.insert_one(message)

    if isinstance(result, results.InsertOneResult):
        if result.inserted_id:
            return (1, 'Message created successfully')
    
    return (0, 'Error creating message entry')


def edit_message_entry(room_id, user_id, new_text):
    result = messages.find({'room_id': room_id, 'from': user_id}).sort('date_created', -1).limit(1)

    for message in result:
        if message is None:
            return (0, 'No messages found')
        
        if message['edited']:
            return (0, 'Message already edited')
        
        res = messages.update_one({'_id': message['_id']}, {'$set': {'text': new_text, 'edited': True}})

        if isinstance(res, results.UpdateResult):
            if res.matched_count == 1:
                return (1, 'Message updated successfully')
        break

    return (0, 'Message not found')


def get_all_messages_by_room(room_id, user_id):
    message_count = messages.count_documents({ '$and': [{'room_id': room_id}, 
        {'$or': [{'to': user_id}, {'from': user_id}]}]
    })

    if message_count == 0:
        return (0, 'No messages found', [])

    all_transcripts = messages.find({ '$and': [{'room_id': room_id}, 
        {'$or': [{'to': user_id}, {'from': user_id}]}]
    }, {'_id': 0}).sort('date_created', -1)

    return (1, 'success', list(all_transcripts))


def get_message(room_id, user_id):
    result = messages.find({'room_id': room_id, 'from': user_id}, {'_id': 0}).sort('date_created', -1).limit(1)

    for message in result:
        if message is None:
            return (0, 'No messages found', None)
        
        return (1, 'success', message)
