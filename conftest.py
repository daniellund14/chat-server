import os
import pytest
from app import db as _db
from app import create_flask_app
from flask_socketio import test_client

basedir = os.path.abspath(os.path.dirname(__file__))

TESTDB = 'test_chat.db'
TESTDB_PATH = f'{basedir}/db/{TESTDB}'
TEST_DATABASE_URI = f'sqlite:////{basedir}/db/{TESTDB}'


@pytest.fixture(scope='session')
def app(request):
    """Creates test app"""
    app = create_flask_app(__name__, 'test_config.Config')

    # Establish an application context before running the tests.
    ctx = app.app_context()
    ctx.push()

    def teardown():
        ctx.pop()

    request.addfinalizer(teardown)
    return app


@pytest.fixture(scope='session')
def db(app, request):
    """Session-wide test database."""
    if os.path.exists(TESTDB_PATH):
        os.unlink(TESTDB_PATH)

    def teardown():
        _db.drop_all()
        os.unlink(TESTDB_PATH)

    _db.app = app
    _db.create_all()

    request.addfinalizer(teardown)
    return _db


@pytest.fixture(scope='function')
def session(db, request):
    """Creates a new database session for a test."""
    connection = db.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection, binds={})
    session = db.create_scoped_session(options=options)

    db.session = session

    def teardown():
        transaction.rollback()
        connection.close()
        session.remove()

    request.addfinalizer(teardown)
    return session


@pytest.fixture(scope='session')
def socketio_client(request, app):
    client = test_client

    def teardown():
        print("SocketIO teardown")

    request.addfinalizer(teardown)
    return client
