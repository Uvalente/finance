from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, FloatField
from wtforms.validators import DataRequired, NumberRange


class QuoteForm(FlaskForm):
    symbol = StringField('Symbol', [DataRequired()])
    submit = SubmitField('Quote')


class BuyForm(FlaskForm):
    symbol = StringField('Symbol', [DataRequired()])
    shares = IntegerField('Shares', [DataRequired(), NumberRange(min=1)])
    buy_price = FloatField('Buy Price', [DataRequired(), NumberRange(min=0.0)])
    submit = SubmitField('Buy')
