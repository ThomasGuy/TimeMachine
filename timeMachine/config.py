import os

# from timeMachine.database.base import db_name
base_dir = os.path.abspath(os.path.dirname(__file__))
delta = '15m'
db_name = f'sqlite:///c:\\data\\sqlite\\db\\tickTocTesting{delta}.db'


class Config(object):
    """Configuration constants"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    DELTA = delta
    DATABASE_URI = os.environ.get('DATABASE_URL') or db_name
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or db_name
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['your-email@example.com']
