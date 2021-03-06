def test_wrong_credential(test_client, init_database):
    response = test_client.post(
        '/login',
        data=dict(username='user', password='pass'),
        follow_redirects=True)

    assert b'Invalid username' in response.data


def test_correct_credential(test_client, init_database):
    response = test_client.post(
        '/login',
        data=dict(username='seed_user', password='seed_password'), follow_redirects=True
    )

    assert b'Logged in' in response.data


def test_logout(test_client, init_database):
    response = test_client.get('/logout', follow_redirects=True)

    assert b'Logged out' in response.data
