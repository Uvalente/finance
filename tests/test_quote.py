from .helpers.utils import log_in, log_out


def test_quote(test_client, init_database):
    log_in(test_client)
    response = test_client.post(
        '/quote',
        data=dict(symbol='AAPL'),
        follow_redirects=True
    )
    assert b'A share of Apple' in response.data
    assert b'cost \xc2\xa3 200.00' in response.data
    log_out(test_client)
