from app import create_flask_app, socketio

app = create_flask_app()

if __name__ == '__main__':
    socketio.run(app)
