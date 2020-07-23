from app.main import routes
from app.models import Stock
from .helpers.utils import log_in, buy_share


def test_sell_share(test_client, init_database, monkeypatch):
    log_in(test_client)

    def value(arg):
        return dict(symbol='AAPL', price='400.00')

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
    print(response.data)
    assert b'800.00' not in response.data
