
from app import socket_io
from flask_socketio import emit, join_room, leave_room, close_room, rooms, disconnect
from flask import request, Response
from flask_cors import cross_origin

@socket_io.on_error_default
@cross_origin(headers='*', supports_credentials=True)
def default_error_handler(e):
    print(f"Error: {e}")
    socket_io.stop()

@socket_io.on('connect')
@cross_origin(headers='*', supports_credentials=True)
def connect():
    emit('connect', {'data': f'User {request.sid} connected'})
    return Response('Client connected!!!!')

@socket_io.on('disconnect')
@cross_origin(headers='*', supports_credentials=True)
def disconnect():
    emit('disconnect', {'data': f'User {request.sid} disconnected'})
    return Response('Client disconnected!!!')

@socket_io.on('message')
@cross_origin(headers='*', supports_credentials=True)
def message(data):
    emit('message', {'id': request.sid, 'data': data}, broadcast=True)
    return Response('OK')

@socket_io.on('mutate')
@cross_origin(headers='*', supports_credentials=True)
def mutate(data):
    emit('mutate', {'id': request.sid, 'roomID': data['roomID']}, broadcast=True)
    return Response('OK')

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