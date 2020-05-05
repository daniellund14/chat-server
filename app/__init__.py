from flask import Flask
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS


socketio = SocketIO(cors_allowed_origins='*')
db = SQLAlchemy()


def create_flask_app(debug=False, config='config.Config'):
    """Create an application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object(config)

    from .chat.views import chat
    app.register_blueprint(chat)

    from .users.views import users
    app.register_blueprint(users)

    from .messages.views import messages
    app.register_blueprint(messages)

    db.init_app(app)

    socketio.init_app(app)
    with app.app_context():
        db.create_all()
        CORS(app, resources={r"/*": {"origins": "*"}})
        return app

