def test_error_creation(test_client, init_database):
    response = test_client.post(
        'register',
        data=dict(username='seed_user', email='test@example.com',
                  password='test_password', confirmPassword='test_password'),
        follow_redirects=True
    )
    assert b'Username already in use' in response.data

    response = test_client.post(
        'register',
        data=dict(username='seed_user_2', email='seed@example.com',
                  password='test_password', confirmPassword='test_password'),
        follow_redirects=True
    )
    assert b'Email already in use' in response.data


def test_user_creation(test_client, init_database):
    response = test_client.post(
        '/register',
        data=dict(username='tester', email='test@example.com',
                  password='test_password', confirmPassword='test_password'),
        follow_redirects=True
    )
    assert b'Registered' in response.data
