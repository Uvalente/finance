from app.models import User
from sqlalchemy import inspect


def test_500_page_and_session_rollback(test_client, init_database):
    user = User(username='user', email='user@example.com')
    user_status = inspect(user)
    init_database.session.add(user)

    assert user_status.pending

    response = test_client.get('/test500')

    assert not user_status.pending
    assert response.status_code == 500
    assert b'An unexpected error has occurred' in response.data
