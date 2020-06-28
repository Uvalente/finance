from app import create_app

app = create_app()


def test():
    response = app.test_client().get('/hello')

    assert response.data == b"Hello world"
