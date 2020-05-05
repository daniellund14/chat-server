from . import db
import uuid
import enum
from datetime import datetime as dt


class UserStatus(enum.Enum):
    ONLINE = 'online'
    OFFLINE = 'offline'


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    status = db.Column(db.Enum(UserStatus), default=UserStatus.OFFLINE)
    created = db.Column(db.Date, default=dt.now())

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'id': self.id,
            'username': self.username,
            'status': self.status.value,
            'created': self.created
        }

    def __repr__(self):
        return f'<User {self.username}>'


def generate_uuid():
    return str(uuid.uuid4())


class PrivateChannel(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uuid = db.Column(db.String, name="uuid", default=generate_uuid)
    room = db.Column(db.String)
    user_1 = db.Column(db.Integer)
    user_2 = db.Column(db.Integer)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'uuid': self.uuid,
            'room': self.room,
            'user_1': self.user_1,
            'user_2': self.user_2
        }


class UserChannel(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer)
    channel_id = db.Column(db.Integer)
    room = db.Column(db.String)

    @property
    def serialize(self):
        return {
            'user_id': self.user_id,
            'channel_id': self.channel_id,
            'room': self.room
        }


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text = db.Column(db.String(280))
    channel_id = db.Column(db.Integer)
    room = db.Column(db.String)
    creating_user = db.Column(db.String)
    receiving_user = db.Column(db.String)
    created = db.Column(db.DateTime, default=dt.now())

    @property
    def serialize(self):
        return {
            'id': self.id,
            'text': self.text,
            'channel_id': self.channel_id,
            'created': self.created
        }

