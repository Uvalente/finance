from .helpers.utils import log_in, log_out


def test_quote(test_client, init_database, monkeypatch):
    log_in(test_client)

    from app.main import routes

    def value(arg):
        return dict(
            symbol='AAPL',
            name='Apple',
            price='200.00'
        )
    monkeypatch.setattr(routes, 'get_quote', value)

    response = test_client.post(
        '/quote',
        data=dict(symbol='AAPL'),
        follow_redirects=True
    )

    assert b'A share of Apple' in response.data
    assert b'cost \xc2\xa3 200.00' in response.data

    log_out(test_client)

def test_wrong_quote(test_client, init_database, monkeypatch):
    log_in(test_client)

    from app.main import routes

    def value(arg):
        return None
    monkeypatch.setattr(routes, 'get_quote', value)

    response = test_client.post(
        '/quote',
        data=dict(symbol='WRONGSYMBOL'),
        follow_redirects=True
    )

    assert b'No stock found' in response.data

    log_out(test_client)
