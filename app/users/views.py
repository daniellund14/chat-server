from flask import Blueprint, request, render_template, session, redirect, url_for, jsonify, Response

from .. import models, db
from ..models import User, UserStatus
from .forms import LoginForm
from . import users_service

users = Blueprint('users', __name__, url_prefix='/users', template_folder='templates')


@users.route('/login', methods=['POST'])
def login_user():
    """
    Login an existing user, or create a user if it doesn't exist and sets status to Online
    :return: Response
    """
    form = LoginForm()
    if request.method == 'POST':
        username = form.username.data
        user = users_service.get_user_from_username(username)
        if user:
            users_service.login_user(username)
        else:
            user = users_service.create_new_user(username)
            users_service.login_user(username)
        return jsonify(user.serialize)


@users.route('/logout', methods=['POST'])
def logout_user():
    """
    Logs out a user, and sets status to Offline
    :return: Response
    """
    request_json = request.get_json()
    username = request_json["username"]
    users_service.logout_user(username)
    return Response("Logged out", status=200)


@users.route('/username/check/<username>', methods=['GET'])
def username_check(username):
    """
    Endpoint to check whether or not a given username is available
    :return: Response - 400 if user exists
    """
    user = users_service.get_user_from_username(username)
    if not user:
        return Response(status=200)
    else:
        return Response("username already exists", status=400)


@users.route('/online')
def get_online_users():
    """
    GET all of the users and IDs that are online
    :return: Response - list of online users
    """
    online_users = models.User.query.filter(User.status == UserStatus.ONLINE).all()
    if online_users:
        return jsonify(online_users=[user.serialize for user in online_users])
    else:
        return {'online_users': []}




