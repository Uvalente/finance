from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_login import UserMixin
from app import db, login


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), index=True,
                         unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    cash = db.Column(db.Integer, default=10000)
    stocks = db.relationship('Stock', backref='owner', lazy=True)
    transactions = db.relationship('Transaction', backref='author', lazy=True)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Stock(db.Model):
    __tablename__ = 'stocks'
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(20), index=True, nullable=False)
    shares = db.Column(db.Integer, nullable=False)
    buy_price = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    transactions = db.relationship('Transaction', backref='stock', lazy=True)

    @classmethod
    def is_owned(cls, symbol, user):
        return Stock.query.filter(
            Stock.symbol == symbol,
            Stock.owner == user
        ).first()

    def __repr__(self):
        return '<Stock {}>'.format(self.symbol)


class Transaction(db.Model):
    __tablename__ = 'transactions'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), index=True, nullable=False)
    stock_id = db.Column(db.Integer, db.ForeignKey('stocks.id'), nullable=False)
    buy_price = db.Column(db.Float)
    sell_price = db.Column(db.Float)
    date_time = db.Column(db.DateTime, nullable=False, default=datetime.now())
    shares = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Transaction {}>'.format(self.date_time)
