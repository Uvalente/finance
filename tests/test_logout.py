def test_logout(test_client, init_database):
    response = test_client.get('/logout', follow_redirects=True)

    assert b'Logged out' in response.data
