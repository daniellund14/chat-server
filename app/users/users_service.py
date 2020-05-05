from .. import db, models


def create_new_user(username: str):
    """
    Creates new user inside the DB
    :param username:
    :return: User
    """
    user = models.User(username=username)
    db.session.add(user)
    db.session.commit()
    return user


def login_user(username: str):
    """
    Updates user status field on User model to Online
    :param username: str
    :return: None
    """
    user = models.User.query.filter_by(username=username).first()
    if not user:
        raise Exception("User not found")
    user.status = models.UserStatus.ONLINE
    db.session.commit()


def logout_user(username: str):
    """
    Updates user status field on User model to Offline
    :param username: str
    :return: None
    """
    user = models.User.query.filter_by(username=username).first()
    if not user:
        raise Exception("User not found")
    user.status = models.UserStatus.OFFLINE
    db.session.commit()


def get_user_from_username(username: str):
    """
    Get User from DB by username
    :param username:
    :return: User
    """
    return models.User.query.filter_by(username=username).first()


def get_user_by_id(user_id: int):
    """
    Get User from DB by user ID
    :param user_id: int
    :return: User
    """
    return models.User.query.filter_by(id=user_id).first()
