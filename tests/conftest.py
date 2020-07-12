import pytest
from app import create_app, db
from app.models import User
from config import TestConfig


@pytest.fixture(scope="module")
def test_client():
    test_app = create_app(TestConfig)
    testing_client = test_app.test_client()

    context = test_app.app_context()
    context.push()

    yield testing_client

    context.pop()

@pytest.fixture(scope="module")
def init_database():
    db.create_all()

    user = User(username='seed_user', email='seed@example.com')
    user.set_password('seed_password')

    db.session.add(user)
    db.session.commit()

    yield db

    db.drop_all()
