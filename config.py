from os import path, environ
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

class Config(object):
    # General Config
    SECRET_KEY = environ.get('SECRET_KEY') or 'secret_random_code'

    # Database Config
    SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI') or \
        'sqlite:///' + path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # IEX Cloud
    IEX_KEY = environ.get('IEX_KEY')


class TestConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
