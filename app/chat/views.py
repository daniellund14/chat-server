from flask import Blueprint, jsonify

from . import chat_service

chat = Blueprint('chat', __name__, url_prefix='/chat', template_folder='templates')


@chat.route('/channels/user/<user_id>', methods=['GET'])
def get_channels(user_id):
    """
    GET channels for a user ID
    :param user_id:
    :return:
    """
    user_channels = chat_service.get_user_channel_by_user_id(int(user_id))
    return jsonify(channels=[channel.serialize for channel in user_channels])
