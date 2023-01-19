from flask import Flask, request
from flask_socketio import SocketIO, emit, join_room
from flask_cors import CORS, cross_origin

app = Flask(__name__)
app.secret_key = '9z$C&F)J@NcRfUjX'
app.debug = True
s_webrtc = SocketIO(app, cors_allowed_origins="*") # socket io webrtc object

# this should work but it refuses to connect
# CORS(app)
# cors = CORS(app, resource={
#     r"/*":{
#         "origins":"*"
#     }
# })

@s_webrtc.on('join')
@cross_origin(headers=["Origin", "Content-Type", "Authorization", "Accept"], supports_credentials=True)
def join(message):
    username = message['username']
    room = message['room'] # flask_socketio uses the concept of "rooms" to have users to connect to
    join_room(room) # flask_socketio method
    print(f'User: {username} has joined the room: {room}')
    emit('ready', {username: username}, to=room, skip_sid=request.sid) #forward username to other person in room
     
@s_webrtc.on('data')
@cross_origin(headers=["Origin", "Content-Type", "Authorization", "Accept"], supports_credentials=True)
def transfer_data(message):
    username = message['username']
    room = message['room']
    data = message['data']
    print(f'Data event from user: {username} has sent the data: {data}')
    emit('data', data, to=room, skip_sid=request.sid) #forward data (video feed) to other person in room
  
@s_webrtc.on_error_default
@cross_origin(headers=["Origin", "Content-Type", "Authorization", "Accept"], supports_credentials=True)
def default_error_handler(e):
    print("Error: {e}")
    s_webrtc.stop()

@s_webrtc.on_error
@cross_origin(headers=["Origin", "Content-Type", "Authorization", "Accept"], supports_credentials=True)
def default_error_handler(e):
    print(f"Error: {e}")
    s_webrtc.stop()
    
if __name__ == '__main__':
    try:
        s_webrtc.run(app, host="0.0.0.0", port=9000)
        
        print(s_webrtc)
    except:
        print("An exception occurred")
    print("started ---------------------------------------------------------------------- ")
    