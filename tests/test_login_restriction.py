def test_index_protection(test_client, init_database):
    response = test_client.get('/', follow_redirects=True)

    assert b'Please log in to access this page' in response.data
    