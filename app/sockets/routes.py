
from app import socket_io
from flask_socketio import emit, join_room, leave_room, close_room, rooms, disconnect
from flask import request, Response
from flask_cors import cross_origin
  
@socket_io.on_error_default
@cross_origin(headers=["Origin", "Content-Type", "Authorization", "Accept"], supports_credentials=True)
def default_error_handler(e):
    print(f"Error: {e}")
    socket_io.stop()

@socket_io.on('connect')
@cross_origin(headers=["Origin", "Content-Type", "Authorization", "Accept"], supports_credentials=True)
def connect():
    print('Client connected!!!')
    return Response('Client connected!!!!')

@socket_io.on('disconnect')
@cross_origin(headers=["Origin", "Content-Type", "Authorization", "Accept"], supports_credentials=True)
def disconnect():
    print('Client disconnected!!!')
    return Response('Client disconnected!!!')

# TODO: Add other routes

# @socket_io.on('create_room', namespace=NAMESPACE)
# def create_room(data):
#     pass


# @socket_io.on('join_room', namespace=NAMESPACE)
# def join_room(data):
#     room_id = data['room_id']
#     user_id = data['user_id']
#     join_room(room_id)


# @socket_io.on('leave_room', namespace=NAMESPACE)
# def leave_room(data):
#     room_id = data['room_id']
#     user_id = data['user_id']

#     users = rooms_api.get_room_users(room_id)

#     if users == None:
#         return

#     # check if user is host
#     if user_id == users[0]:
#         # close room
#         socketio.close_room(room_id, namespace=NAMESPACE)

#         for user in users:
#             socketio.disconnect(user, namespace=NAMESPACE)
#     else:
#         socketio.leave_room(user_id, room_id, namespace=NAMESPACE)
#         socketio.disconnect(user_id, namespace=NAMESPACE)


# @socket_io.on('send_message', namespace=NAMESPACE)
# def send_message(data):
#     room_id = data['room_id']
#     user_id = data['user_id']
#     message = data['message']