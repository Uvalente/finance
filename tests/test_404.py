def test_404_page(test_client):
    response = test_client.get('/randompage')

    assert response.status_code == 404
    assert b"404" in response.data
    assert b"Page Not Found" in response.data
