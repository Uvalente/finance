from app.models import Stock
from .helpers.utils import log_in, log_out


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

    assert stock.symbol == 'AAPL'
    assert stock.shares == 2
    assert stock.buy_price == 200.00
    assert stock.user_id == 1
    print(response.data)
    assert b'You bought 2 AAPL shares at \xc2\xa3 200.00 each' in response.data

    log_out(test_client)
