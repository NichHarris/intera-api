
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