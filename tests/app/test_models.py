import pytest

from app import models


def test_user_model(session):
    user = models.User(username="test")

    session.add(user)
    session.commit()

    assert user


def test_user_model_missing_username(session):
    user = models.User()

    session.add(user)
    with pytest.raises(Exception):
        session.commit()


def test_private_channel_create(session):
    channel = models.PrivateChannel(room="test")

    session.add(channel)
    session.commit()

    assert channel


def test_user_channel_create(session):
    user_channel = models.UserChannel(user_id=1, channel_id=1, room="test")

    session.add(user_channel)
    session.commit()

    assert user_channel


def test_message_create(session):
    text = "test text message"
    channel_id = 1
    room = "test_room"
    creating_user = "user1"
    receiving_user = "user2"
    message = models.Message(
        text=text,
        channel_id=channel_id,
        room=room,
        creating_user=creating_user,
        receiving_user=receiving_user,
    )

    session.add(message)
    session.commit()

    assert message
