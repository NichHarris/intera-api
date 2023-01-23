import random
import os
import json
import argparse
import sys

# add app module to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.rooms import controller as rooms_api
from app.practice_module import controller as practice_api
from app.transcripts import controller as transcripts_api
from config import Database
from pymongo import errors, results

# get a reference to the databases
intera_calls_db = Database.client[Database.intera_calls_db]
intera_practice_db = Database.client[Database.intera_practice_db]

# get a reference to the collections
try: 
    rooms = intera_calls_db[Database.rooms_collection]
    messages = intera_calls_db[Database.messages_collection]
    words = intera_practice_db[Database.word_data_collection]
except errors.CollectionInvalid as err:
    print(err)

def update_rooms(method, field, value=None):
    if method == 'add':
        # get all entries in rooms and add the field "field" with value "value" to each entry
        rooms.update_many({}, {"$set": {field: value}})

    elif method == 'remove':
        # get all entries in rooms and remove the field "field" from each entry
        rooms.update_many({}, {'$unset': {field:1}} , upsert=False)

    # elif method == 'update':
    #     # get all entries in rooms and update the field "field" with value "value" for each entry
    #     rooms.update({}, {'$set': {field: value}} , {'multi': True})

        
    print(method, field, value)


def update_messages(method, field, value=None):
    # get all entries in rooms and add the field "field" with value "value" to each entry
    if method == 'add':
        messages.update_many({}, {"$set": {field: value}})

    elif method == 'remove':
        # get all entries in rooms and remove the field "field" from each entry
        messages.update_many({}, {'$unset': {field:1}}, upsert=False)


def update_words(method, field, value=None):
    # get all entries in rooms and add the field "field" with value "value" to each entry
    if method == 'add':
        words.update_many({}, {"$set": {field: value}})

    elif method == 'remove':
        # get all entries in rooms and remove the field "field" from each entry
        words.update_many({}, {'$unset': {field:1}} , upsert=False)


if __name__ == "__main__":
    print("--------------------------------------------------------------------------------------")
    
    parser = argparse.ArgumentParser()
    # users.json => {'users': [{'name': 'Jason', 'type': 'STT'}, {'name': 'Tom', 'type': 'STT'} ....]
    parser.add_argument('--file', '-f', type=str, default=None, help='File to update collection with => Ex: update_db.py -f updates.json')

    parser.add_argument('--rooms', '-r', action='store_true', help='Update rooms collection')
    parser.add_argument('--messages', '-m', action='store_true', help='Update messages collection')
    parser.add_argument('--words', '-w', action='store_true', help='Update words collection')

    parser.add_argument('--add', '-a', type=str, default=None, help='Add a field to collection => Ex: upgrade_db.py --rooms -a <new_field> -s ')
    parser.add_argument('--remove', '-rm', type=str, default=None, help='Remove a field from collection => Ex: upgrade_db.py --rooms -rm <field_to_remove>')
    # parser.add_argument('--update', '-u', type=str, default=None, help='Update a field in collection => Ex: upgrade_db.py --rooms -u <field_to_update> -s')

    parser.add_argument('--string', '-s', action='store_true', help='Default value to update field with')
    parser.add_argument('--int', '-i', action='store_true', help='Default value to update field with')
    # parser.add_argument('--float', '-fl', action='store_true', help='Default value to update field with => Ex: ')
    # parser.add_argument('--list', '-l', action='store_true', help='Default value to update field with => Ex: ')
    # parser.add_argument('--dict', '-d', action='store_true', help='Default value to update field with => Ex: ')
    parser.add_argument('--bool', '-b', type=str, default=None, help='Default value to update field with')
    args = parser.parse_args()

    collection = None
    if args.rooms:
        collection = 'rooms'
    elif args.messages:
        collection = 'messages'
    elif args.words:
        collection = 'words'


    if collection:
        method = None
        field = None
        value = None
        if args.add:
            method = 'add'
            field = args.add
            if args.string:
                value = ''
            elif args.int:
                value = 0
            elif args.bool:
                value = args.bool.lower() == 'true'
        # elif args.update:
        #     method = 'update'
        #     field = args.update
        #     if args.string:
        #         value = ''
        #     elif args.int:
        #         value = 0
        #     elif args.bool:
        #         value = args.bool.lower() == 'true'
        elif args.remove:
            method = 'remove'
            field = args.remove
        
        if method and field:
            eval(f'update_{collection}("{method}", "{field}", {value})')
        else:
            print(f'Invalid method for {collection} collection.')
    else:
        print('Invalid collection.')
        print('See collection structure under "db_structure.json" in root directory.')

    print(args)
