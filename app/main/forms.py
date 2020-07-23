from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, NumberRange
from wtforms.widgets.html5 import NumberInput


class QuoteForm(FlaskForm):
    symbol = StringField('Symbol', [DataRequired()])
    submit = SubmitField('Quote')


class BuyForm(FlaskForm):
    symbol = StringField('Symbol', [DataRequired()])
    shares = IntegerField('Shares', [DataRequired(), NumberRange(
        min=1)], widget=NumberInput(min=1))
    submit = SubmitField('Buy')
