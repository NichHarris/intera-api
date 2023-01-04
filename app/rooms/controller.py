from config import Database
from pymongo import errors, results
from bson.json_util import dumps
from os import environ as env
from dotenv import find_dotenv, load_dotenv
from datetime import datetime
import uuid
import certifi

# load the environment variables from the .env file
load_dotenv(find_dotenv())

# get a reference to the databases
intera_calls_db = Database.client[Database.intera_calls_db]

# get a reference to the collections
try: 
    rooms = intera_calls_db[Database.rooms_collection]
except errors.CollectionInvalid as err:
    print(err)


# generate a random room_id using the uuid library
def generate_room_id():
    # Get 8 digits of the uuid
    random_id = str(uuid.uuid4())[:8]

    while rooms.count_documents({'room_id': random_id}) != 0:
        random_id = str(uuid.uuid4())[:8]

    return random_id


def create_room(room_id, user_id, host_type):
    room = {'room_id': room_id, 'users': [user_id], 'host_type': host_type, 'date_created': datetime.now(), 'active': True, 'messages': []}
    
    try:
        result = rooms.insert_one(room)
    except errors.DuplicateKeyError as err:
        return (err.code, err._message)
    except errors.PyMongoError as err:
        return (0, err._message)

    if isinstance(result, results.InsertOneResult):
        if result.inserted_id is not None:
            return (1, 'Room successfully created')
        else:
            return (0, 'Room not created')

    return (0, 'Error creating room')

def validate_room(room_id, user_id):
    room = rooms.find_one({'room_id': room_id})

    if room is None:
        return (0, 'Room does not exist')
    
    if room['active'] == False:
        return (0, 'Room is inactive')

    if len(room['users']) == 2:
        if user_id in room['users']:
            return (1, f'User is registered in room')
        else:
            return (0, 'User not registered in room. Room is full')
    
    return (1, 'Room is valid')


def register_user_in_room(room_id, user_id):
    try:
        room = rooms.find_one({'room_id': room_id})
    except errors.PyMongoError as err:
        return (0, err._message)

    if room is None:
        return (0, 'Room does not exist')

    room_users = room['users']

    if len(room_users) == 2:
        return (0, 'Room is full')
    else:
        if user_id in room_users:
            return (0, 'User already registered in room')

        room_users.append(user_id)

        try:
            rooms.update_one({'_id': room['_id']}, {'$set': {'users': room_users}})
        except errors.PyMongoError as err:
            return (0, err._message)
        
    return (1, 'User successfully registered in room')


def get_room(room_id):
    try:
        room = rooms.find_one({'room_id': room_id}, {'_id': 0})
    except errors.PyMongoError as err:
        return (0, err._message, None)
    
    if room is None:
        return (0, 'Room does not exist', None)
    
    return (1, 'success', room)


def update_room_status(room_id, status):
    try:
        room = rooms.find_one({'room_id': room_id})
    except errors.PyMongoError as err:
        return (0, err._message)

    if room is None:
        return (0, 'Room does not exist')
    
    try:
        rooms.update_one({'_id': room['_id']}, {'$set': {'active': status}})
    except errors.DuplicateKeyError as err:
        return (err.code, err._message)
    except Exception as err:
        return (0, str(err))

    return (1, 'Room status successfully updated')        


def get_room_users(room_id):
    pass


def add_room_messages(room_id, messages):
    try:
        room = rooms.find_one_and_update({'room_id': room_id}, {'$push': {'messages': messages}})
    except errors.PyMongoError as err:
        return (0, err._message)
    
    if room is None:
        return (0, 'Room does not exist')

    return (1, 'success')


def get_all_rooms():
    try:
        all_rooms = rooms.find()
    except errors.PyMongoError as err:
        return (0, err._message, None)
    except errors.DocumentTooLarge as err:
        return (0, str(err), None)
    except Exception as err:
        return (0, str(err), None)
    
    return (1, 'success', list(all_rooms))


def get_all_rooms_by_id(user_id):
    try:
        all_rooms = rooms.find({ '$and': [{'users': user_id}, {'active': False}]}, {'_id': 0}).sort('date_created', -1)
    except errors.PyMongoError as err:
        return (0, err._message, [])
    except errors.DocumentTooLarge as err:
        return (0, str(err), [])
    except Exception as err:
        return (0, str(err) , [])

    return (1, 'success', list(all_rooms))