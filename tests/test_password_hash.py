from app.models import User


def test_password_hash(test_db):
    user = User(username='Umberto', email='umberto@example.com')
    user.set_password('password')

    assert user.password_hash != 'password'
    assert user.check_password('password')

    test_db.session.add(user)
    test_db.session.commit()

    db_user = User.query.filter_by(username=user.username).first()

    assert user.email == db_user.email
    