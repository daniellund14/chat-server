from flask_socketio import emit, join_room, leave_room
from .. import socketio
from . import chat_service
from ..users import users_service
from ..messages import messages_service


@socketio.on('joined', namespace='/chat')
def joined(message):
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""
    print("joined")
    # room = 'test'
    # join_room(room)


@socketio.on('create username', namespace='/chat')
def username_created(message):
    """
    A new username has been created and connected to the channels
    :param message: message containing username
    :return: None
    """
    username = message["username"]
    users_service.create_new_user(username)


@socketio.on('create room', namespace='/chat')
def create_room(message):
    """
    User created a new private message channel. Create PrivateChannel inside DB
    and emit new room message
    :param message: message containing information to create room
        REQUIRES: room, user_id_1, user_id_2 fields
    :return: None
    """
    room = message["room"]
    user_id_1 = message["user_id_1"]
    user_id_2 = message["user_id_2"]
    channel = chat_service.get_private_channel_for_users(user_id_1, user_id_2)
    if channel:
        # do nothing channel exists - this is likely an error
        emit("room exists", {
            "msg": "room you are trying to create already exists",
            "room": channel.serialize
        })
        return
    channel = chat_service.create_private_channel(room, user_id_1, user_id_2)

    # Add each user channel entry
    chat_service.add_user_channel(channel, user_id_1)
    chat_service.add_user_channel(channel, user_id_2)
    emit("room created", {"room": room, "user_id_1": user_id_1, "user_id_2": user_id_2})


@socketio.on('message', namespace='/chat')
def message_handler(message):
    """Sent by a client when the user entered a new message.
    The message is sent to all people in the room."""
    creating_user = message["from"]
    receiving_user = message["to"]
    room = message["room"]
    text = message["text"]
    channel = chat_service.get_private_channel_by_room_name(room)
    if not channel:  # For simplicity catching generic exception
        emit("message error", {'msg': 'new message failed to post', 'reason': 'room name does not exist'})
        return
    messages_service.create_message(text, room, creating_user, receiving_user, channel=channel)
    emit('new message', {'display_text': f'{creating_user} {text}'}, room=room)


@socketio.on('left', namespace='/chat')
def left(message):
    """Sent by clients when they leave a room.
    A status message is broadcast to all people in the room."""
    username = message['username']
    room = message['room']
    leave_room(room)
    emit('status', {'msg': f'{username}', 'status': 'offline'}, room=room)
