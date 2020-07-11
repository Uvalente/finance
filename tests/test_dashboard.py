def test_initial_cash(test_client, init_database):
    response = test_client.post(
        '/login',
        data=dict(username='seed_user', password='seed_password'), follow_redirects=True
    )

    assert b'Total' in response.data
    assert b'CASH' in response.data
    assert b'10000' in response.data
    response = test_client.get('/logout', follow_redirects=True)
