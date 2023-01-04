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

SPEAKER = "STT"
SIGNER = "ASL"

def populate_rooms(controller):
    host_type = SIGNER
    user_type = SPEAKER

    for _ in range(n):
        host_id = random.choice(host_user_ids)
        guest_id = random.choice(guest_user_ids)

        room_id = controller.generate_room_id()

        #print(f'Room ID: {room_id}')

        result, message = controller.create_room(room_id, host_id, host_type)

        if result == 1:
            result, message = controller.register_user_in_room(room_id, guest_id)

            print(f'RoomID: {room_id} GuestID: {guest_id}: {message}')

        else:
            print(f'RoomID {room_id}: {message}')

        # switch the user types so that we get good dummy data
        temp_host_type = host_type
        host_type = user_type
        user_type = temp_host_type

def populate_msgs(controller_room, controller_trans):
    result, message, data = controller_room.get_all_rooms()

    if result == 1:
        for room in data:
            room_id = room["room_id"]
            
            host_type = room["host_type"]
            guest_type = SPEAKER if host_type == SIGNER else SIGNER
            
            room_length = len(room["users"])
            
            if room_length == 2:
                host_info = [room["users"][0], host_type]
                guest_info = [room["users"][1], guest_type]

                from_user_info = host_info
                to_user_info =  guest_info

                for _ in range(n):
                    message_to_send = random.choice(messages)

                    from_id = from_user_info[0]
                    to_id = to_user_info[0]
                    message_type = from_user_info[1]

                    #print(f'Room ID: {room_id}')

                    result, message = controller_trans.create_message_entry(room_id, from_id, to_id, message_to_send, False, message_type, True)

                    print(f'RoomID: {room_id}: {message}')
                    # switch the from and to user info so that we get good dummy data
                    # essentially for every iteration of the inner for loop we change
                    # who is receiving and sending the message
                    temp_from_user_info = from_user_info
                    from_user_info = to_user_info
                    to_user_info = temp_from_user_info
            else:
                print(f"Room {room_id} is a test room with {room_length} users.")
    else:
        print(f'Getting all rooms failed: {message}')

def populate_words(controller):
    for word, url in words.items():
        result, message = controller.create_word_entry(word, url)

        print(message)

if __name__ == "__main__":
    # comment out the method u want to run or run all 3 if you want to
    
    # populate_rooms(rooms_api)

    # populate_msgs(rooms_api, transcripts_api)

    populate_words(practice_api)
