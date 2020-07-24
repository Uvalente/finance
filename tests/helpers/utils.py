def log_in(client):
    client.post(
        '/login',
        data=dict(username='seed_user', password='seed_password'), follow_redirects=True
    )


def log_out(client):
    client.get('/logout', follow_redirects=True)


def buy_share(client, symbol, shares):
    client.post(
        '/buy',
        data=dict(symbol=symbol, shares=shares),
        follow_redirects=True
    )
