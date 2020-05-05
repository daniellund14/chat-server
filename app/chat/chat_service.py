from .. import models
from .. import db


def create_private_channel(room: str, user_id_1: int, user_id_2: int):
    """
    Create a new PrivateChannel model in the DB
    :param room: str, name of room
    :param user_id_1: int
    :param user_id_2: int
    :return: PrivateChannel
    """
    channel = models.PrivateChannel(room=room, user_1=user_id_1, user_2=user_id_2)
    db.session.add(channel)
    db.session.commit()
    return channel


def get_private_channel_for_users(user_id_1: int, user_id_2: int):
    """
    Get the private channel between two user ids
    :param user_id_1: int
    :param user_id_2: int
    :return: PrivateChannel model or None if channel does not exist
    """
    channel = models.PrivateChannel.query.filter_by(
        user_1=user_id_1, user_2=user_id_2
    ).first()
    if not channel:
        # Check for users being flipped
        channel = models.PrivateChannel.query.filter_by(
            user_1=user_id_2, user_2=user_id_1
        ).first()
    return channel


def get_private_channel_by_room_name(name: str):
    """
    GET channel by a room name
    :param name: str for room name
    :return: PrivateChannel
    """
    channel = models.PrivateChannel.query.filter_by(
        room=name
    ).first()
    return channel


def add_user_channel(channel: models.PrivateChannel, user_id: int):
    """
    Create UserChannel for mappings of users and channels
    :param channel: Channel - existing channel
    :param user_id: int
    :return: None
    """
    user_channel = models.UserChannel(user_id=user_id, channel_id=channel.id, room=channel.room)
    db.session.add(user_channel)
    db.session.commit()


def get_user_channel_by_user_id(user_id: int):
    """
    Get UserChannel model for a user id
    :param user_id: int
    :return: UserChannel
    """
    return models.UserChannel.query.filter_by(user_id=user_id).all()

