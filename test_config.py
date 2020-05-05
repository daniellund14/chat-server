from os import path

basedir = path.abspath(path.dirname(__file__))


class Config:
    """Set Flask configuration variables from .env file."""
    SECRET_KEY = 'gjr39dkjn344_!67#'
    FLASK_ENV = 'test'
    FLASK_DEBUG = 1

    # Database
    SQLALCHEMY_DATABASE_URI = f'sqlite:////{basedir}/db/test_chat.db'
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
