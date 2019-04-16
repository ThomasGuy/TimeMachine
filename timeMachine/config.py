import os

base_dir = os.path.abspath(os.path.dirname(__file__))
db_name = 'sqlite:///c:\\data\\sqlite\\db\\tickToc15m.db'
remoteSQL = 'mysql+pymysql://TomRoot:Sporty66@mysql.stackcp.com:51228/ticktoctestDB-3637742e'
master = 'sqlite:///c:\\data\\sqlite\\db\\master_db.db'


class Config(object):
    """Configuration constants"""
    APIKEY = '484cb8d70ed62517ecfec5b4666fb83c8e62944a4b460222d72becd39d6e4412'
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    DELTA = '15m'
    HOUR = '1h'
    OUTSIDER = '3h'
    DATABASE_URI = master
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or MySqlDB
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['twguy66@gmail.com']
