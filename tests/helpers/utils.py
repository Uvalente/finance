def log_in(client):
    client.post(
        '/login',
        data=dict(username='seed_user', password='seed_password'), follow_redirects=True
    )


def log_out(client):
    client.get('/logout', follow_redirects=True)
