from app import models
from app.messages import messages_service
from datetime import datetime, timedelta


def test_create_message(db, session):
    messages_service.create_message(
        text="text",
        room="test",
        creating_user="user1",
        receiving_user="user2",
        channel=models.PrivateChannel()
    )

    messages = models.Message.query.all()

    assert len(messages) > 0

    _cleanup_all_models(db, session)


def test_get_all_messages_no_filter(db, session):
    _insert_message(session, "message 1")
    _insert_message(session, "message 2")

    messages = messages_service.get_all_messages()

    assert len(messages) == 2

    _cleanup_all_models(db, session)


def test_get_all_messages_count_filter(db, session):
    for i in range(120):
        _insert_message(session, f'message {i}')

    messages = messages_service.get_all_messages(filter_type='count')

    assert len(messages) == 100

    _cleanup_all_models(db, session)


def test_get_all_messages_days_filter(db, session):
    old_date = datetime.now() - timedelta(days=40)
    for i in range(100):
        _insert_message(session, f'message {i}')
    for i in range(30):
        _insert_message(session, f'message {1}', date=old_date)

    messages = messages_service.get_all_messages(filter_type='days')

    assert len(messages) == 100

    _cleanup_all_models(db, session)


def test_get_recent_messages_from_to(db, session):
    _insert_user(session, "user1")
    _insert_user(session, "user2")

    _insert_message(session, text="message 1")
    _insert_message(session, text="message 2")

    messages = messages_service.get_recent_messages_from_to(creator="user1", receiver="user2")

    assert len(messages) == 2

    _cleanup_all_models(db, session)


def test_get_recent_messages_from_to_none(db, session):
    _insert_user(session, "user1")
    _insert_user(session, "user2")

    _insert_message(session, text="message 1")
    _insert_message(session, text="message 2")

    messages = messages_service.get_recent_messages_from_to(creator="user2", receiver="user1")

    assert len(messages) == 0

    _cleanup_all_models(db, session)


def test_get_recent_messages_to_from_multiple(db, session):
    _insert_user(session, "user1")
    _insert_user(session, "user2")

    _insert_message(session, text="message 1", creating_user="user2", receiving_user="user1")
    _insert_message(session, text="message 2", creating_user="user2", receiving_user="user1")
    _insert_message(session, text="message 3", creating_user="user2", receiving_user="user1")
    _insert_message(session, text="message 2", creating_user="user1", receiving_user="user2")

    messages = messages_service.get_recent_messages_from_to(creator="user2", receiver="user1")

    assert len(messages) == 3

    messages = messages_service.get_recent_messages_from_to(creator="user1", receiver="user2")

    assert len(messages) == 1

    _cleanup_all_models(db, session)


def test_get_messages_from_room(db, session):
    _insert_message(session, room="test_room")

    messages = messages_service.get_messages_from_room("test_room")

    assert len(messages) == 1


def test_get_messages_from_room_none(db, session):
    messages = messages_service.get_messages_from_room("test_room")

    assert len(messages) == 0


def _insert_user(session, username):
    user = models.User(username=username)

    session.add(user)
    session.commit()


def _insert_message(
        session,
        text="test",
        date=datetime.now(),
        creating_user="user1",
        receiving_user="user2",
        room="room"
):
    """
    Util function to build a message inside the DB any field is overridable
    :param session: required
    :param text: str
    :param date: datetime
    :param creating_user: str
    :param receiving_user: str
    :param room: str
    :return:
    """
    message = models.Message(
        text=text,
        channel_id=1,
        room=room,
        creating_user=creating_user,
        receiving_user=receiving_user,
        created=date
    )
    session.add(message)
    session.commit()


# This isn't great, but for sake of time remove all models
def _cleanup_all_models(db, session):
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        print(f'Clear table {table}')
        session.execute(table.delete())
    session.commit()
