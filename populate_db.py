import uuid
from app.rooms import controller as rooms_api
from app.practice_module import controller as practice_api
from app.transcripts import controller as transcripts_api
# # import app.rooms.controller as rooms_api
# import app.practice_module.controller as practice_api
# import app.transcripts.controller as transcripts_api
import random
import sys

host_user_ids = ["Nick", "Abdul", "Matt", "Lisa", "Sharon", "Tarun", "Ali", "James", "Ben", "Samantha"]#[str(uuid.uuid4()) for _ in range(n)]
guest_user_ids = ["Jim", "Jennifer", "Wade", "Chris", "Padme", "Tony", "Pepper", "Wilson", "Joe", "Jessica"]#[str(uuid.uuid4()) for _ in range(n)]

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
                "est laborum.",
                "Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium",
                "totam rem aperiam",
                "eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo.",
                "Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit",
                "sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt.",
                "Neque porro quisquam est", 
                "qui dolorem ipsum quia dolor sit amet",
                "consectetur, adipisci velit",
                "sed quia non numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem.",
                "Ut enim ad minima veniam,",
                "quis nostrum exercitationem ullam corporis suscipit laboriosam,",
                "nisi ut aliquid ex ea commodi consequatur?",
                "Quis autem vel eum iure reprehenderit qui in ea voluptate velit esse quam nihil molestiae consequatur",
                "vel illum qui dolorem eum fugiat quo voluptas nulla pariatur?",
                "Sed repellendus rerum quo aliquid cumque et adipisci voluptates ",
                "eum fuga tempora qui porro repellat qui sint rerum.",
                "Ex totam tempore est esse accusamus rem iste cupiditate!"
                "Ut earum ratione non excepturi expedita ea neque quia id quia",
                "quidem et aliquid atque?",
                "Qui quidem veniam ut deserunt dignissimos",
                "in vitae facere aut distinctio",
                "consequatur qui aliquam assumenda",
                "ut voluptatem eaque et nesciunt nihil."
            ] # 35 messages

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

    for _ in range(len(host_user_ids)):
        host_id = random.choice(host_user_ids)
        guest_id = random.choice(guest_user_ids)

        room_id = controller.generate_room_id()
        
        result, message = controller.create_room(room_id, host_id, host_type)

        if result == 1:
            result, message = controller.register_user_in_room(room_id, guest_id)

            print(f'RoomID: {room_id} HostID: {host_id} GuestID: {guest_id}: {message}')

        else:
            print(f'RoomID {room_id}: {message}')

        controller.update_room_status(room_id, False)
        # switch the user types so that we get good dummy data
        # temp_host_type = host_type
        # host_type = user_type
        # host_type, user_type = user_type, host_type
        host_type, user_type = user_type, host_type

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

                for _ in range(len(messages)):
                    message_to_send = random.choice(messages)

                    from_id = from_user_info[0]
                    to_id = to_user_info[0]
                    message_type = from_user_info[1]

                    result, message = controller_trans.create_message_entry(room_id, from_id, to_id, message_to_send, False, message_type, True)

                    print(f'RoomID: {room_id}: {message}')
                    # switch the from and to user info so that we get good dummy data
                    # essentially for every iteration of the inner for loop we change
                    # who is receiving and sending the message
                    from_user_info, to_user_info = to_user_info, from_user_info

                controller_room.update_room_status(room_id, False)

                messages_room = controller_trans.get_all_messages_by_room(room_id)
                controller_room.add_room_messages(room_id, messages_room[2])
            else:
                print(f"Room {room_id} is a test room with {room_length} users.")

    else:
        print(f'Getting all rooms failed: {message}')

def populate_words(controller):
    for word, url in words.items():
        result, message = controller.create_word_entry(word, url)

        print(message)

def populate_db_with_info(host_name, host_type, controller_room, controller_trans):
    guest_name = random.choice(guest_user_ids)

    room_id = controller_room.generate_room_id()

    result_room, message_room = controller_room.create_room(room_id, host_name, host_type)

    if result_room == 1:
        register_result, register_message = controller_room.register_user_in_room(room_id, guest_name)

        print(f'RoomID: {room_id} GuestID: {guest_name}: {register_message}')

        if register_result == 1:
            guest_type = SPEAKER if host_type == SIGNER else SIGNER

            host_info = [host_name, host_type]
            guest_info = [guest_name, guest_type]

            from_user_info = host_info
            to_user_info =  guest_info

            for _ in range(len(messages)):
                message_to_send = random.choice(messages)

                from_name = from_user_info[0]
                to_name = to_user_info[0]
                message_type = from_user_info[1]

                result, create_message = controller_trans.create_message_entry(room_id, from_name, to_name, message_to_send, False, message_type, True)

                print(f'RoomID: {room_id}: {create_message}')
                from_user_info, to_user_info = to_user_info, from_user_info
            
            controller_room.update_room_status(room_id, False)
            messages_room = controller_trans.get_all_messages_by_room(room_id)
            controller_room.add_room_messages(room_id, messages_room[2])
        else:
           print(f'RoomID {room_id}: {register_message}') 
        
    else:
        print(f'RoomID {room_id}: {message_room}')




if __name__ == "__main__":
    print("--------------------------------------------------------------------------------------")
    print(sys.argv)
    
    # supply 2 arguements in this order
    # host_name: String => Ex: Jason, Abdul, etc
    # host_type: String => Ex: ASL, STT
    # Ex execution: populate_db.py Jason STT
    #             : populate_db.py Will ASL
    if len(sys.argv) > 2: 
        host_name = sys.argv[1]
        host_type = sys.argv[2]
        
        print(f'{host_name} {host_type}')
        populate_db_with_info(host_name, host_type, rooms_api, transcripts_api)
    else:
        print("Default script run.")
        # comment out the method u want to run or run all 3 if you want to
        
        #populate_rooms(rooms_api)

        populate_msgs(rooms_api, transcripts_api)

        # populate_words(practice_api)


    # host_name = "Abdul2"
    # host_type = SIGNER
    
    
    # populate_db_with_info(host_name, host_type, rooms_api, transcripts_api)
