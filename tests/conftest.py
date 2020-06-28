from app import create_app, db
from config import Config

import pytest


@pytest.fixture(scope="module")
def test_db():
    class TestConfig(Config):
        TESTING = True
        SQLALCHEMY_DATABASE_URI = 'sqlite://'

    app = create_app(TestConfig)
    context = app.app_context()
    context.push()
    db.create_all()

    yield db

    db.session.remove()
    db.drop_all()
    context.pop()
