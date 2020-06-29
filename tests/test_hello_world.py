def test(client):
    response = client.get('/hello')

    assert response.data == b"Hello world"
