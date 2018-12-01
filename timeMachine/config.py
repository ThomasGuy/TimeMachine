import os

base_dir = os.path.abspath(os.path.dirname(__file__))
db_name = f'sqlite:///c:\\data\\sqlite\\db\\tickToc15m.db'
db_name2 = f'sqlite:///c:\\data\\sqlite\\db\\master_db.db'
MySqlDB = 'mysql+pymysql://TomRoot:Sporty66@mysql.stackcp.com:51228/ticktoctestDB-3637742e'
localDB = f'sqlite:///c:\\data\\sqlite\\db\\master_db.db'


class Config(object):
    """Configuration constants"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    DELTA = '15m'
    OUTSIDER = '3h'
    HOUR = '1h'
    DATABASE_URI = MySqlDB
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or MySqlDB
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['twguy66@gmail.com']
