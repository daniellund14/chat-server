import pytest

from app import models
from app.chat import events


def test_create_username(db, session):
    message = {'username': "test"}
    events.username_created(message)

    user = models.User.query.filter_by(username="test").first()

    assert user

    _cleanup_all_models(db, session)


def test_create_username_missing_username(db, session):
    message = {}
    with pytest.raises(Exception):
        events.username_created(message)

    user = models.User.query.filter_by(username="test").first()

    assert not user

    # Future check for emit call (SocketIO testing?)

    _cleanup_all_models(db, session)


def _create_user(session, _id, username="user"):
    user = models.User(id=_id, username=username)
    session.add(user)
    session.commit()


# This isn't great, but for sake of time remove all models
def _cleanup_all_models(db, session):
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        print(f'Clear table {table}')
        session.execute(table.delete())
    session.commit()
