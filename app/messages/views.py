from flask import Blueprint, jsonify, request

from . import messages_service

messages = Blueprint('messages', __name__, url_prefix='/messages', template_folder='templates')


@messages.route('/all', methods=['GET'])
def get_all_messages():
    """
    GET request for all messages with optional filter_type
        - count = last 100 messages
        - days = all messages within the last 30 days
        - none
    :return: list of messages
    """
    filter_type = request.args.get('filter_type')
    all_messages = messages_service.get_all_messages(filter_type)
    return jsonify(messages=[message.serialize for message in all_messages])


@messages.route('/from/<creator>/to/<receiver>', methods=['GET'])
def get_recent_messages_from_to(creator: str, receiver: str):
    """
        GET request for all messages from one send to another
        :return: list of messages
        """
    all_messages = messages_service.get_recent_messages_from_to(creator=creator, receiver=receiver)
    return jsonify(messages=[message.serialize for message in all_messages])


@messages.route('/room/<room_name>', methods=['GET'])
def get_messages_from_room(room_name):
    """
    GET all messages for a given room
    :param room_name: name of room to get messages from
    :return:
    """
    all_messages = messages_service.get_messages_from_room(room_name=room_name)
    return jsonify(messages=[message.serialize for message in all_messages])
