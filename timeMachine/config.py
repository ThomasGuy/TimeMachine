import os

base_dir = os.path.abspath(os.path.dirname(__file__))
db_name = f'sqlite:///c:\\data\\sqlite\\db\\tickToc15m.db'
MySqlDB = 'mysql+pymysql://TomRoot:Sporty66@mysql.stackcp.com:51228/ticktoctestDB-3637742e'


class Config(object):
    """Configuration constants"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    DELTA = '15m'
    OUTSIDER = '3h'
    HOUR = '1h'
    DATABASE_URI = db_name
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or db_name
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['twguy66@gmail.com']
