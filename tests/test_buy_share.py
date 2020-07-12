from app.models import Stock, User
from .helpers.utils import log_in


def test_buy_share(test_client, init_database, monkeypatch):
    log_in(test_client)

    from app.main import routes
    def value(arg):
        return dict(price='200.00')

    monkeypatch.setattr(routes, 'get_quote', value)

    response = test_client.post(
        '/buy',
        data=dict(symbol='AAPL', shares=2),
        follow_redirects=True
    )

    stock = Stock.query.get(1)
    user = User.query.get(1)

    assert stock.symbol == 'AAPL'
    assert stock.shares == 2
    assert stock.buy_price == 200.00
    assert stock.user_id == 1
    assert b'You bought 2 AAPL shares at \xc2\xa3 200.00 each' in response.data
    assert user.cash == 9600

def test_bought_share(test_client, init_database, monkeypatch):
    from app.main import routes
    def value(arg):
        return dict(name='Apple, Inc.', price='350.00')

    monkeypatch.setattr(routes, 'get_quote', value)

    response = test_client.get('/index')
    print(response.data)
    assert b'700.00' in response.data
    assert b'350.00' in response.data
    assert b'9600.00' in response.data
    assert b'10300.00' in response.data
    assert b'Apple, Inc.' in response.data
