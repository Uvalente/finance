from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from app.models import User


class LoginForm(FlaskForm):
    username = StringField('Username', [DataRequired()])
    password = PasswordField('Password', [DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           [
                               DataRequired(),
                               Length(min=3)
                           ])
    email = StringField('Email',
                        [
                            Length(min=6),
                            Email(message='Enter a valid email'),
                            DataRequired()
                        ])
    password = PasswordField('Password',
                             [
                                 DataRequired(),
                                 Length(min=6)
                             ])
    confirmPassword = PasswordField('Confirm Password',
                                    [
                                        EqualTo('password', message='Password must match')
                                    ])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already in use')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already in use')
