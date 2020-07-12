from app.models import Stock
from .helpers.utils import log_in, log_out


def test_buy_share(test_client, init_database):
    log_in(test_client)

    response = test_client.post(
        '/buy',
        data=dict(symbol='AAPL', shares=2, buy_price=200.00),
        follow_redirects=True
    )

    stock = Stock.query.get(1)

    assert stock.symbol == 'AAPL'
    assert stock.shares == 2
    assert stock.buy_price == 200.00
    assert stock.user_id == 1
    assert b'You bought 2 AAPL shares' in response.data

    log_out(test_client)
