from app import socket_io
from flask_socketio import emit, join_room, leave_room, close_room, disconnect, send
from flask import request, Response
from flask_cors import cross_origin

from app.rooms import controller as rooms_api
from app.transcripts import controller as transcripts_api
from app.auth import controller as auth

@socket_io.on('connect')
@cross_origin(headers=["Origin", "Content-Type", "Authorization", "Accept"], supports_credentials=True)
def connect():
    emit('connect', {'data': f'User {request.sid} connected'}, skip_sid=request.sid)
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
    emit('ready', {user: user}, to=room_id, skip_sid=request.sid)    
    return Response(f'{request.sid} has joined room id {room_id}.')

@socket_io.on('leave')
@cross_origin(headers=["Origin", "Content-Type", "Authorization", "Accept"], supports_credentials=True)
def leave(data):
    room_id = data['room_id'] if 'room_id' in data else ''
    user = data['user'] if 'user' in data else ''
    
    # check if username is host -> if so, delete room
    emit('disconnect', {'data': f'{user} has left the room id: {room_id}.', 'user_sid': request.sid}, broadcast=True, to=room_id, skip_sid=request.sid)
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

@socket_io.on('data_transfer')
def data_transfer(data):
    room_id = data['room_id']
    body = data['body']
    emit('data_transfer', body, broadcast=True, to=room_id, skip_sid=request.sid)
    return Response(f'Transferred data for room {room_id}')