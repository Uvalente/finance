from app.main import routes
from app.models import Stock
from .helpers.utils import log_in, buy_share


def value(arg):
    return dict(symbol='AAPL', price='400.00')


def test_sell_share(test_client, init_database, monkeypatch):
    log_in(test_client)

    monkeypatch.setattr(routes, 'get_quote', value)

    buy_share(test_client, 'AAPL', 2)

    stock = Stock.query.get(1)
    assert stock.shares == 2
    response = test_client.post(
        '/sell',
        data=dict(symbol='AAPL', shares=1),
        follow_redirects=True
    )

    stock = Stock.query.get(1)
    assert stock.shares == 1
    assert b'800.00' not in response.data
    assert b'10000.00' in response.data
    assert b'You sold 1 AAPL shares at \xc2\xa3 400.00 each'


def test_over_sell_error(test_client, init_database, monkeypatch):
    monkeypatch.setattr(routes, 'get_quote', value)

    response = test_client.post(
        '/sell',
        data=dict(symbol='AAPL', shares=20),
        follow_redirects=True
    )

    stock = Stock.query.get(1)
    assert stock.shares == 1
    assert b'You do not have enough shares to sell' in response.data


def test_selling_all_shares(test_client, init_database, monkeypatch):
    monkeypatch.setattr(routes, 'get_quote', value)

    test_client.post(
        '/sell',
        data=dict(symbol='AAPL', shares=1)
    )

    def new_value(arg):
        return dict(symbol='AAPL', price=555.55)

    monkeypatch.setattr(routes, 'get_quote', new_value)

    response = test_client.get('/')

    stock = Stock.query.filter_by(symbol='AAPL').first()

    assert stock.shares == 0
    assert b'555.55' not in response.data
