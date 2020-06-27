from app import app

def test():
  response = app.test_client().get('/hello')

  assert response.data == b"Hello world"