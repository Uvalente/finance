from app.main import routes
from app.models import Transaction, Stock
from .helpers.utils import log_in, buy_share

def aapl(arg):
    return dict(symbol='AAPL', price='300.00')

def nvda(arg):
    return dict(symbol='NVDA', price='750.00')

def test_transaction_seed(test_client, init_database):
    log_in(test_client)

    amzn_stock = Stock(
        symbol='AMZN',
        shares=3,
        buy_price=44.44,
        user_id=1
    )
    amzn_buy = Transaction(
        user_id=1,
        stock_id=1,
        buy_price=44.44,
        shares=2
    )
    amzn_sell = Transaction(
        user_id=1,
        stock_id=1,
        sell_price=70.00,
        shares=1
    )

    init_database.session.add(amzn_stock)
    init_database.session.add(amzn_buy)
    init_database.session.add(amzn_sell)
    init_database.session.commit()

    response = test_client.get('/history')
    print(response.data)
    assert b'AMZN' in response.data
    assert b'44.44' in response.data
    assert b'2' in response.data
    assert b'70.00' in response.data
    assert b'2020' in response.data
