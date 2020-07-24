from flask import render_template, current_app, flash, redirect, url_for
from flask_login import login_required, current_user
import requests
from app import db
from app.main import main_bp
from app.models import Stock
from .forms import QuoteForm, BuyForm, SellForm


@main_bp.route("/hello")
def hello():
    return "Hello world"


@main_bp.route('/')
@main_bp.route('/index')
@login_required
def index():
    stocks = []
    total = current_user.cash
    for stock in current_user.stocks:
        item = get_quote(stock.symbol)
        item['shares'] = stock.shares
        val = item['shares'] * float(item['price'])
        item['price'] = f"{float(item['price']):0.2f}"
        item['total'] = f"{val:0.2f}"
        stocks.append(item)
        total += val

    total = f"{total:0.2f}"
    cash = f"{current_user.cash:0.2f}"
    return render_template('index.html', cash=cash, stocks=stocks, total=total)


@main_bp.route('/quote', methods=['GET', 'POST'])
@login_required
def quote():
    quote_form = QuoteForm()
    buy_form = BuyForm()
    if quote_form.validate_on_submit():
        share = get_quote(quote_form.symbol.data)
        if not share:
            flash('No stock found')
            return redirect(url_for('main_bp.quote'))
        return render_template('quote.html', quote_form=quote_form, share=share, buy_form=buy_form)

    return render_template('quote.html', quote_form=quote_form)


@main_bp.route('/buy', methods=['POST'])
@login_required
def buy():
    form = BuyForm()
    if form.validate_on_submit():
        query_symbol = form.symbol.data
        query_quantity = form.shares.data
        share = get_quote(query_symbol)
        buy_price = float(share['price'])

        transaction_value = buy_price * query_quantity
        if transaction_value > current_user.cash:
            flash('Not enough cash to proceed with the purchase')
            return redirect(url_for('main_bp.quote'))

        owned_stock = Stock.is_owned(query_symbol, current_user)
        if owned_stock:
            owned_stock.shares += query_quantity
        else:
            stock = Stock(
                symbol=query_symbol,
                shares=query_quantity,
                buy_price=buy_price,
                owner=current_user
            )
            db.session.add(stock)

        current_user.cash -= transaction_value
        db.session.commit()

        flash(
            f"You bought {query_quantity} {query_symbol} shares at £ {buy_price:0.2f} each"
        )
        return redirect(url_for('main_bp.index'))

    flash('Something went wrong, please try again')
    return redirect(url_for('main_bp.quote'))


@main_bp.route('/sell', methods=['GET', 'POST'])
@login_required
def sell():
    form = SellForm()
    choices = [(stock.symbol, stock.symbol) for stock in current_user.stocks]
    form.symbol.choices = choices

    if form.validate_on_submit():
        query_symbol = form.symbol.data
        query_quantity = form.shares.data

        owned_stock = Stock.is_owned(query_symbol, current_user)

        if not owned_stock:
            flash('You do not own this stock')
            return redirect(url_for('main_bp.sell'))

        if query_quantity > owned_stock.shares:
            flash('You do not have enough shares to sell')
            return redirect(url_for('main_bp.sell'))

        share = get_quote(query_symbol)
        sell_price = float(share['price'])

        flash(
            f"You sold {query_quantity} {query_symbol} shares at {sell_price:0.2f} each"
        )
        current_user.cash += query_quantity * sell_price

        if query_quantity == owned_stock.shares:
            stock = Stock.query.filter_by(
                symbol=query_symbol, user_id=current_user.id).first()
            db.session.delete(stock)
        else:
            owned_stock.shares -= query_quantity

        db.session.commit()
        return redirect(url_for('main_bp.index'))

    return render_template('sell.html', form=form)


def get_quote(symbol):
    # MAY NEED TO PARSE SYMBOL WITH urllib.parse.quote_plus()
    try:
        # USING TESTING API KEY
        api_key = current_app.config['TEST_IEX_KEY']
        # USING SANDBOX API
        response = requests.get(
            f'https://sandbox.iexapis.com/stable/stock/{symbol}/quote?token={api_key}')
        response.raise_for_status()
    except requests.RequestException:
        return None

    try:
        data = response.json()
        return dict(
            symbol=data['symbol'],
            name=data['companyName'],
            price=data['latestPrice']
        )
    except (KeyError, TypeError, ValueError):
        return None
