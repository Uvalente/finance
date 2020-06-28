import os
import tempfile
import pytest

from wsgi import app
from config import Config
from app import create_app, db


@pytest.fixture(scope="module")
def test_db():
    class TestConfig(Config):
        TESTING = True
        SQLALCHEMY_DATABASE_URI = 'sqlite://'

    _app = create_app(TestConfig)
    context = _app.app_context()
    context.push()
    db.create_all()

    yield db

    db.session.remove()
    db.drop_all()
    context.pop()


@pytest.fixture(scope="module")
def client():
    db_fd, app.config['SQLALCHEMY_DATABASE_URI'] = tempfile.mkstemp()
    app.config['TESTING'] = True

    with app.test_client() as client:
        # with app.app_context():
        #     init_db()
        yield client

    os.close(db_fd)
    os.unlink(app.config['SQLALCHEMY_DATABASE_URI'])
