from app import socket_io
from flask_socketio import emit, join_room, leave_room, close_room, rooms, disconnect, send
from flask import request, Response
from flask_cors import cross_origin

from app.rooms import controller as rooms_api
from app.transcripts import controller as transcripts_api
from app.auth import controller as auth
  
@socket_io.on_error_default
@cross_origin(headers=["Origin", "Content-Type", "Authorization", "Accept"], supports_credentials=True)
def default_error_handler(e):
    print(f"Error: {e}")
    socket_io.stop()

@socket_io.on('connect')
@cross_origin(headers=["Origin", "Content-Type", "Authorization", "Accept"], supports_credentials=True)
def connect():
    emit('connect', {'data': f'User {request.sid} connected'}, skip_sid=request.sid)
    return Response('Client connected!!!!')

@socket_io.on('disconnect')
@cross_origin(headers=["Origin", "Content-Type", "Authorization", "Accept"], supports_credentials=True)
def disconnect():
    emit('disconnect', {'data': f'User {request.sid} disconnected'})
    return Response('Client disconnected!!!')


@socket_io.on('join')
@cross_origin(headers=["Origin", "Content-Type", "Authorization", "Accept"], supports_credentials=True)
def join(data):    

    room_id = data['room_id']

    join_room(room_id)
    print(f'{request.sid} has entered the room id: {room_id}.')
    emit('join', {'data': f'{request.sid} has entered the room id: {room_id}.', 'user_sid': request.sid}, to=room_id, skip_sid=request.sid)
    return Response(f'{request.sid} has entered the room id: {room_id}.')

@socket_io.on('leave')
@cross_origin(headers=["Origin", "Content-Type", "Authorization", "Accept"], supports_credentials=True)
def leave(data):
    room_id = data['room_id']
    username = data['username']
    
    # check if username is host -> if so, delete room
    if rooms_api.is_host(room_id, username):
        emit('close_room', {'data': f'Room {room_id} has been closed.'}, to=room_id, skip_sid=request.sid)
        close_room(room_id)
    else:
        emit('disconnect', {'data': f'{request.sid} has left the room id: {room_id}.', 'user_sid': request.sid}, to=room_id)
    leave_room(room_id)
    return Response('OK')

@socket_io.on('message')
@cross_origin(headers=["Origin", "Content-Type", "Authorization", "Accept"], supports_credentials=True)
def message(data):
    emit('message', {'id': request.sid, 'data': data}, broadcast=True, to_room=data['room_id'], skip_sid=request.sid)
    return Response('OK')

@socket_io.on('mutate')
@cross_origin(headers=["Origin", "Content-Type", "Authorization", "Accept"], supports_credentials=True)
def mutate(data):
    emit('mutate', {'id': request.sid, 'roomID': data['roomID']}, broadcast=True, to_room=data['roomID'], skip_sid=request.sid)
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