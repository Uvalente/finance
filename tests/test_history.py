from freezegun import freeze_time
from datetime import datetime
from app.main import routes
from app.models import Transaction, Stock
from .helpers.utils import log_in, buy_share

def aapl(arg):
    return dict(symbol='AAPL', price='300.00')


def nvda(arg):
    return dict(symbol='NVDA', price='750.00')

@freeze_time("2020-07-10 15:30:20")
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
        shares=2,
        date_time=datetime.now()
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
    assert b'10/07/2020' in response.data
    assert b'15:30:20' in response.data


def test_buy_history(test_client, init_database, monkeypatch):
    log_in(test_client)

    monkeypatch.setattr(routes, 'get_quote', aapl)

    buy_share(test_client, 'AAPL', 2)

    monkeypatch.setattr(routes, 'get_quote', nvda)

    buy_share(test_client, 'NVDA', 4)

    response = test_client.get('/history')

    assert b'AAPL' in response.data
    assert b'NVDA' in response.data
    assert b'300.00' in response.data
    assert b'750.00' in response.data
    assert b'2' in response.data
    assert b'4' in response.data


def test_sell_history(test_client, init_database, monkeypatch):
    def sell_aapl(arg):
        return dict(symbol='AAPL', price='310.00')

    monkeypatch.setattr(routes, 'get_quote', sell_aapl)

    test_client.post(
        '/sell',
        data=dict(symbol='AAPL', shares=1),
        follow_redirects=True
    )

    def sell_aapl_two(arg):
        return dict(symbol='AAPL', price='275.58')

    monkeypatch.setattr(routes, 'get_quote', sell_aapl_two)

    test_client.post(
        '/sell',
        data=dict(symbol='AAPL', shares=1),
        follow_redirects=True
    )

    response = test_client.get('/history')

    print(response.data)
    assert b'310.00' in response.data
    assert b'275.58' in response.data
