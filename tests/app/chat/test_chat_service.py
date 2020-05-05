from app import models
from app.chat import chat_service


def test_create_private_channel(db, session):
    chat_service.create_private_channel(room="test", user_id_1=1, user_id_2=2)

    channels = models.PrivateChannel.query.all()
    assert len(channels) > 0

    _cleanup_all_models(db, session)


def test_get_private_channel_for_users(db, session):
    _create_private_channel(session)
    channel = chat_service.get_private_channel_for_users(user_id_1=1, user_id_2=2)

    assert channel

    _cleanup_all_models(db, session)


def test_get_private_channel_for_users_no_channel(session):
    channel = chat_service.get_private_channel_for_users(user_id_1=1, user_id_2=2)

    assert not channel


def test_get_channel_by_room_name(db, session):
    _create_private_channel(session)

    channel = chat_service.get_private_channel_by_room_name("test")

    assert channel

    _cleanup_all_models(db, session)


def test_get_channel_by_room_name_no_room(session):
    channel = chat_service.get_private_channel_by_room_name("bad")

    assert not channel


def test_add_user_channel(db, session):
    private_channel = _create_private_channel(session)
    chat_service.add_user_channel(channel=private_channel, user_id=1)

    created = models.UserChannel.query.all()

    assert len(created) > 0

    _cleanup_all_models(db, session)


def test_get_user_channel_by_user_id(db, session):
    _create_user_channel(session)

    channel = chat_service.get_user_channel_by_user_id(1)

    assert channel

    _cleanup_all_models(db, session)


def test_get_user_channel_by_user_id_none(db, session):
    channel = chat_service.get_user_channel_by_user_id(1)

    assert not channel


def _create_private_channel(session):
    private_channel = models.PrivateChannel(room="test", user_1=1, user_2=2)

    session.add(private_channel)
    session.commit()

    return private_channel


def _create_user_channel(session):
    user_channel = models.UserChannel(room="test", channel_id=1, user_id=1)

    session.add(user_channel)
    session.commit()

    return user_channel


# This isn't great, but for sake of time remove all models
def _cleanup_all_models(db, session):
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        print(f'Clear table {table}')
        session.execute(table.delete())
    session.commit()
