from .. import db, models
from ..users import users_service
from datetime import datetime, timedelta


def create_message(text: str, room: str, creating_user: str, receiving_user: str, channel: models.PrivateChannel):
    """
    Create a new message inside the database
    :param text: message to be displayed
    :param room: str for room name
    :param creating_user: username of creating user
    :param receiving_user: username of receiving user
    :param channel: Channel Model
    :return: None
    """
    message = models.Message(
        text=text,
        creating_user=creating_user,
        receiving_user=receiving_user,
        channel_id=channel.id,
        room=room
    )
    db.session.add(message)
    db.session.commit()


def get_all_messages(filter_type: str = ""):
    """
    GET all messages regardless of sender, or room
    :param filter_type: filter on messages, if none is provided get all (USE ALL WITH CAUTION)
        - count: gets 100 recent messages
        - days: gets all messages within the last 30 days
    :return: list(Message)
    """
    if filter_type == 'count':
        messages = models.Message.query.limit(100).all()
    elif filter_type == 'days':
        messages = models.Message.query.filter(
            models.Message.created >= datetime.now() - timedelta(days=30)
        ).all()
    else:
        messages = models.Message.query.all()
    return messages


def get_recent_messages_from_to(creator: str, receiver: str):
    """
    Get all stored messages in DB for a given sender to a receiver
    :param creator: username for creator
    :param receiver: username for receiver
    :return: list(Message)
    """
    creating_user = users_service.get_user_from_username(creator)
    receiving_user = users_service.get_user_from_username(receiver)
    if not creating_user or not receiving_user:
        raise Exception("username does not exist")
    messages = models.Message.query.filter_by(creating_user=creator, receiving_user=receiver).all()
    return messages


def get_messages_from_room(room_name: str):
    """
    Get all stored messages in DB for a given room, limit 100
    :param room_name:
    :return: list(Message)
    """
    return models.Message.query.order_by(models.Message.created).filter_by(room=room_name).limit(100).all()
