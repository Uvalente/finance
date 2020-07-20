from flask import render_template, current_app, flash, redirect, url_for
from flask_login import login_required, current_user
import requests
from app import db
from app.main import main_bp
from app.models import Stock
from .forms import QuoteForm, BuyForm


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
        share = get_quote(form.symbol.data)
        print(share)
        # IF USER HAS STOCK -> UPDATE
        # ELSE CREATE
        owned_stock = Stock.query.filter(Stock.symbol == form.symbol.data, Stock.owner == current_user).first()
        if owned_stock:
            owned_stock.shares += form.shares.data
        else:
            stock = Stock(
                symbol=form.symbol.data,
                shares=form.shares.data,
                buy_price=share['price'],
                owner=current_user
            )
            db.session.add(stock)
        
        current_user.cash -= float(share['price']) * form.shares.data
        db.session.commit()

        flash(f"You bought {form.shares.data} {share['symbol']} shares at £ {float(share['price']):0.2f} each")
        return redirect(url_for('main_bp.index'))
    flash('Something went wrong, please try again')
    return redirect(url_for('main_bp.quote'))


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
