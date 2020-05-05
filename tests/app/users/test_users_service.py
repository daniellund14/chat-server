import pytest

from app import models
from app.users import users_service


def test_create_new_user(db, session):
    users_service.create_new_user("test")

    user = models.User.query.filter_by(username="test").first()

    assert user

    _cleanup_all_models(db, session)


def test_login_user(db, session):
    username = "user1"
    _insert_user(session, username=username)

    users_service.login_user(username)

    user = models.User.query.filter_by(username=username).first()

    assert user.status == models.UserStatus.ONLINE

    _cleanup_all_models(db, session)


def test_login_user_not_found(db, session):
    username = "user1"

    with pytest.raises(Exception):
        users_service.login_user(username)

    _cleanup_all_models(db, session)


def test_logout_user(db, session):
    username = "user1"
    _insert_user(session, username=username)

    users_service.logout_user(username)

    user = models.User.query.filter_by(username=username).first()

    assert user.status == models.UserStatus.OFFLINE

    _cleanup_all_models(db, session)


def test_logout_user_not_found(db, session):
    username = "user1"

    with pytest.raises(Exception):
        users_service.logout_user(username)

    _cleanup_all_models(db, session)


def test_get_user_from_username(db, session):
    username = "test_user"
    _insert_user(session, username=username)

    user = users_service.get_user_from_username(username)

    assert user

    _cleanup_all_models(db, session)


def test_get_user_from_username_none(db, session):
    user = users_service.get_user_from_username("nope")

    assert not user

    _cleanup_all_models(db, session)


def test_get_user_by_id(db, session):
    _id = 1
    _insert_user(session, _id=_id)

    user = users_service.get_user_by_id(_id)

    assert user

    _cleanup_all_models(db, session)


def test_get_user_by_id_none(db, session):
    _id = 2
    _insert_user(session, _id=_id)

    user = users_service.get_user_by_id(1)

    assert not user

    _cleanup_all_models(db, session)


def _insert_user(session, username="test", _id=1):
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
