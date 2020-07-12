from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class QuoteForm(FlaskForm):
    symbol = StringField('Symbol', [DataRequired()])
    submit = SubmitField('Quote')
