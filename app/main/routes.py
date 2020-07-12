from flask import render_template
from flask_login import login_required, current_user
from app.main import main_bp
from .forms import QuoteForm


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
        share = dict(symbol='AAPL', name='Apple', price='200.00')
        return render_template('quote.html', quote_form=quote_form, share=share)

    return render_template('quote.html', quote_form=quote_form)
