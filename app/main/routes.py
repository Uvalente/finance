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
    return render_template('index.html', user=current_user)


@main_bp.route('/quote', methods=['GET', 'POST'])
@login_required
def quote():
    quote_form = QuoteForm()
    if quote_form.validate_on_submit():
        share = get_quote(quote_form.symbol.data)
        if not share:
            flash('No stock found')
            return redirect(url_for('main_bp.quote'))
        return render_template('quote.html', quote_form=quote_form, share=share)

    return render_template('quote.html', quote_form=quote_form)


@main_bp.route('/buy', methods=['POST'])
@login_required
def buy():
    form = BuyForm()
    if form.validate_on_submit():
        stock = Stock(
            symbol=form.symbol.data,
            shares=form.shares.data,
            buy_price=form.buy_price.data,
            owner=current_user
        )
        db.session.add(stock)
        db.session.commit()
        flash(f'You bought {stock.shares} {stock.symbol} shares')
        return redirect(url_for('main_bp.index'))


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
