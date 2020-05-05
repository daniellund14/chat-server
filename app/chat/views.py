from flask import Blueprint, render_template, session, redirect, url_for, request, jsonify

from .forms import LoginForm
from .. import db, models
from . import chat_service

chat = Blueprint('chat', __name__, url_prefix='/chat', template_folder='templates')


@chat.route('/', methods=['GET', 'POST'])
def index():
    form = LoginForm()
    if form.validate_on_submit():
        user = models.User(username=form.username.data)
        db.session.add(user)
        session['username'] = form.username.data
        db.session.add(channel)
        db.session.commit()
        session['room'] = form.room.data
        return redirect(url_for('.message'))
    elif request.method == 'GET':
        form.username.data = session.get('username', '')
        form.room.data = session.get('room', '')
    return render_template('index.html', form=form)


@chat.route('/message')
def message():
    """Chat room. The user's name and room must be stored in
    the session."""
    username = session.get('username', '')
    room = session.get('room', '')
    if username == '' or room == '':
        return redirect(url_for('.index'))
    online_users = models.User.query.filter(models.User.status == models.UserStatus.ONLINE).all()
    print(f'online users:{online_users}')
    return render_template('chat.html', username=username, room=room, users=online_users)


@chat.route('/channels/user/<user_id>', methods=['GET'])
def get_channels(user_id):
    user_channels = chat_service.get_user_channel_by_user_id(int(user_id))
    return jsonify(channels=[channel.serialize for channel in user_channels])


@chat.route('/tester', methods=['GET'])
def get_tester():
    return render_template('chat.html')
