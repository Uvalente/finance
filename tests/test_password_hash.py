from app import db
from app.models import User

def test_password_hash():
    user = User(username='Umberto', email='umberto@example.com')
    user.hash_password('password')

    assert user.password_hash != 'password'
    assert user.check_password('password') == True
