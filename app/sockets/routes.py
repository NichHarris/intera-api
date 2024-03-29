# Flask and Sockets
from app import socket_io
from flask_socketio import emit, join_room, leave_room, rooms
from flask import request, Response
from flask_cors import cross_origin

@socket_io.on('connect')
@cross_origin(headers=["Origin", "Content-Type", "Authorization", "Accept"], supports_credentials=True)
def connect():
    emit('connect',  {'test': 'test'})
    return Response('Client connected')

@socket_io.on('disconnect')
@cross_origin(headers=["Origin", "Content-Type", "Authorization", "Accept"], supports_credentials=True)
def disconnect():
    emit('disconnect', {'data': f'User {request.sid} disconnected'})
    return Response('Client disconnected')

@socket_io.on('join')
@cross_origin(headers=["Origin", "Content-Type", "Authorization", "Accept"], supports_credentials=True)
def join(data):
    user = data['user'] if 'user' in data else ''
    room_id = data['room_id'] if 'room_id' in data else ''

    join_room(room_id)
    print(f'Joining room {room_id} with user {user} sid: {request.sid}')
    emit('pong', {'join': room_id, 'rooms': rooms()}, broadcast=True, to=room_id)
    emit('ready', broadcast=True, to=room_id, skip_sid=request.sid)   
    return Response(f'{request.sid} has joined room id {room_id}.')

@socket_io.on('join_msg')
@cross_origin(headers=["Origin", "Content-Type", "Authorization", "Accept"], supports_credentials=True)
def join_msg(data):
    user = data['user'] if 'user' in data else ''
    room_id = data['room_id'] if 'room_id' in data else ''

    join_room(room_id)
    emit('mutate', {'user': user, 'room_id': room_id}, broadcast=True, to_room=room_id, skip_sid=request.sid)
    return Response('OK')

@socket_io.on('leave')
@cross_origin(headers=["Origin", "Content-Type", "Authorization", "Accept"], supports_credentials=True)
def leave(data):
    room_id = data['room_id'] if 'room_id' in data else ''
    user = data['user'] if 'user' in data else ''

    print(f'Leaving room {room_id} with user {user} sid: {request.sid}')
    emit('disconnect', {'data': f'{user} has left the room id: {room_id}.', 'user_sid': request.sid}, broadcast=True, to=room_id, skip_sid=request.sid)

    # if rooms_api.is_host(user, room_id):
    #     print('Host has left the room. Closing room.')
    emit('leave', {'user': user, 'user_sid': request.sid}, broadcast=True, to=room_id)

    leave_room(room_id)
    return Response('OK')

@socket_io.on('ping')
@cross_origin(headers=["Origin", "Content-Type", "Authorization", "Accept"], supports_credentials=True)
def ping(data):
    room_id = data['room_id'] if 'room_id' in data else ''
    user = data['user'] if 'user' in data else ''
    
    emit('pong', {'data': f'Pong from room {room_id} for user {user}'}, broadcast=True, to=request.sid)
    return Response('OK')

@socket_io.on('message')
@cross_origin(headers=["Origin", "Content-Type", "Authorization", "Accept"], supports_credentials=True)
def message(data):
    room_id = data['room_id'] if 'room_id' in data else ''
    join_room(room_id)
    emit('mutate', {'id': request.sid, 'data': data}, broadcast=True, to_room=data['room_id'], skip_sid=request.sid)
    return Response('OK')

@socket_io.on('ready')
@cross_origin(headers=["Origin", "Content-Type", "Authorization", "Accept"], supports_credentials=True)
def ready(data):
    emit('ready', {'id': request.sid, 'data': data}, broadcast=True, to_room=data['room_id'], skip_sid=request.sid)
    return Response('OK')

@socket_io.on('mutate')
@cross_origin(headers=["Origin", "Content-Type", "Authorization", "Accept"], supports_credentials=True)
def mutate(data):
    room_id = data['room_id'] if 'room_id' in data else ''
    print('received mutate')
    emit('mutate', {'id': request.sid, 'roomID': room_id}, broadcast=True, to_room=room_id, skip_sid=request.sid)
    return Response('OK')

@socket_io.on('data_transfer')
def data_transfer(data):
    room_id = data['room_id']
    # emit('data_transfer', data['body'], to=room_id, skip_sid=request.sid)
    emit('data_transfer', data, to=room_id, skip_sid=request.sid)
    return Response(f'Transferred data for room {room_id}')

@socket_io.on('stream_buffer')
def stream_buffer(data):
    room_id = data['room_id']

    # Testing
    emit('stream_buffer_response', data)
    return Response(f'Received stream buffer data for room {room_id}')