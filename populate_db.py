import uuid
import app.rooms.controller as rooms_api
import app.practice_module.controller as practice_api
import app.transcripts.controller as transcripts_api
import random

n = 5
host_user_ids = [str(uuid.uuid4()) for _ in range(n)]
guest_user_ids = [str(uuid.uuid4()) for _ in range(n)]

messages = [
                "Lorem ipsum dolor sit amet",
                "consectetur adipiscing elit",
                "sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
                "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut",
                "aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in",
                "voluptate velit esse cillum dolore eu fugiat nulla pariatur.",
                "Excepteur sint occaecat cupidatat non proident",
                "sunt in culpa qui",
                "officia",
                "deserunt",
                "mollit anim id",
                "est laborum."
            ]

words = {
            "hello": "https://www.youtube.com/watch?v=uKKvNqA9N20", 
            "bye": "https://www.youtube.com/watch?v=4rOC5fNt-_k", 
            "please": "https://www.youtube.com/watch?v=wtNN6H27L3k", 
            "thank you": "https://www.youtube.com/watch?v=IvRwNLNR4_w", 
            "water": "https://www.youtube.com/watch?v=-SdOfxGhb0A"
        }

# TODO Update, should just call the actual api roots to do this, that way we can test them simulatenously
def populate_rooms(db):
    for _ in range(n):
        host_id = random.choice(host_user_ids)        
        guest_id = random.choice(guest_user_ids)  
        
        room_id = db.create_room(host_id)
        
        print(f'Room ID: {room_id}')
        
        if room_id is not None:
            registered = db.register_user_in_room(room_id, guest_id)
            
            if registered: 
                print(f'GuestID {guest_id} successfully registered')
            else:
                print(f'GuestID {guest_id} not successfully registered')
        else:
            print(f'Room not created') 

# TODO Update, should just call the actual api roots to do this, that way we can test them simulatenously
def populate_msgs(db):
    rooms = db.room # needs to be changed to a method that gets all the rooms
    for room_id in rooms:
        for _ in range(n):
            host_id = random.choice(host_user_ids)        
            guest_id = random.choice(guest_user_ids)  
            message = random.choice(messages) 
            
            print(f'Room ID: {room_id}')
            
            db.create_transcript_entry(room_id, guest_id, host_id, message)

# TODO Update, should just call the actual api roots to do this, that way we can test them simulatenously
def populate_words(db):
    for word, url in words.items():
        db.create_word_entry(word, url)
                             
if __name__ == "__main__":

    populate_rooms(rooms_api)
    
    populate_msgs(transcripts_api)
    
    populate_words(practice_api)
