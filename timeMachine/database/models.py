from datetime import datetime

# Third party imports
from sqlalchemy import Table, Column, DateTime, Float, String, Integer, create_engine
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from flask_sqlalchemy_session import current_session
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# TimaMachine imports
from timeMachine.server import login


# delta = '15m'
# db_name = f'sqlite:///c:\\data\\sqlite\\db\\tickTocTest{delta}.db'
Base = declarative_base()


class User(UserMixin, Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(64), index=True, unique=True)
    email = Column(String(120), index=True, unique=True)
    password_hash = Column(String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id):
    return current_session.query(User).get(int(id))


class MyMixin(object):

    @declared_attr
    def __tablename__(cls): # pylint: disable=E0213
        return cls.__name__.lower()

    __table_args__ = {'mysql_engine': 'Sqlite'}
    __mapper_args__ = {'always_refresh': True}

    id = Column(Integer(), primary_key=True)
    MTS = Column(DateTime(), nullable=False)
    Open = Column(Float(), nullable=False)
    Close = Column(Float(), nullable=False)
    High = Column(Float(), nullable=False)
    Low = Column(Float(), nullable=False)
    Volume = Column(Float(), nullable=False)


class Avt(MyMixin, Base):
    def __repr__(self):
        return "<Btc(MTS='%s', Open='%f', Close='%f')>" % (
            self.MTS, self.Open, self.Close)

class Bch(MyMixin, Base):
    def __repr__(self):
        return "<Btc(MTS='%s', Open='%f', Close='%f')>" % (
            self.MTS, self.Open, self.Close)

class Btc(MyMixin, Base):
    def __repr__(self):
        return "<Btc(MTS='%s', Open='%f', Close='%f')>" % (
            self.MTS, self.Open, self.Close)

class Btg(MyMixin, Base):
    def __repr__(self):
        return "<Btc(MTS='%s', Open='%f', Close='%f')>" % (
            self.MTS, self.Open, self.Close)
            
class Dsh(MyMixin, Base):
    def __repr__(self):
        return "<Btc(MTS='%s', Open='%f', Close='%f')>" % (
            self.MTS, self.Open, self.Close)
            
class Eos(MyMixin, Base):
    def __repr__(self):
        return "<Eos(MTS='%s', Open='%f', Close='%f')>" % (
            self.MTS, self.Open, self.Close)
            
class Etc(MyMixin, Base):
    def __repr__(self):
        return "<Eos(MTS='%s', Open='%f', Close='%f')>" % (
            self.MTS, self.Open, self.Close)

class Eth(MyMixin, Base):
    def __repr__(self):
        return "<Eth(MTS='%s', Open='%f', Close='%f')>" % (
            self.MTS, self.Open, self.Close)

class Fun(MyMixin, Base):
    def __repr__(self):
        return "<Eth(MTS='%s', Open='%f', Close='%f')>" % (
            self.MTS, self.Open, self.Close)

class Gnt(MyMixin, Base):
    def __repr__(self):
        return "<Eth(MTS='%s', Open='%f', Close='%f')>" % (
            self.MTS, self.Open, self.Close)

class Iot(MyMixin, Base):
    def __repr__(self):
        return "<Iot(MTS='%s', Open='%f', Close='%f')>" % (
            self.MTS, self.Open, self.Close)

class Ltc(MyMixin, Base):
    def __repr__(self):
        return "<Ltc(MTS='%s', Open='%f', Close='%f')>" % (
            self.MTS, self.Open, self.Close)

class Neo(MyMixin, Base):
    def __repr__(self):
        return "<Neo(MTS='%s', Open='%f', Close='%f')>" % (
            self.MTS, self.Open, self.Close)

class Qsh(MyMixin, Base):
    def __repr__(self):
        return "<Neo(MTS='%s', Open='%f', Close='%f')>" % (
            self.MTS, self.Open, self.Close)

class Qtm(MyMixin, Base):
    def __repr__(self):
        return "<Neo(MTS='%s', Open='%f', Close='%f')>" % (
            self.MTS, self.Open, self.Close)

class Omg(MyMixin, Base):
    def __repr__(self):
        return "<Omg(MTS='%s', Open='%f', Close='%f')>" % (
            self.MTS, self.Open, self.Close)

class Rcn(MyMixin, Base):
    def __repr__(self):
        return "<Omg(MTS='%s', Open='%f', Close='%f')>" % (
            self.MTS, self.Open, self.Close)

class Rlc(MyMixin, Base):
    def __repr__(self):
        return "<Omg(MTS='%s', Open='%f', Close='%f')>" % (
            self.MTS, self.Open, self.Close)

class San(MyMixin, Base):
    def __repr__(self):
        return "<Omg(MTS='%s', Open='%f', Close='%f')>" % (
            self.MTS, self.Open, self.Close)

class Spk(MyMixin, Base):
    def __repr__(self):
        return "<Omg(MTS='%s', Open='%f', Close='%f')>" % (
            self.MTS, self.Open, self.Close)

class Trx(MyMixin, Base):
    def __repr__(self):
        return "<Trx(MTS='%s', Open='%f', Close='%f')>" % (
            self.MTS, self.Open, self.Close)

class Xlm(MyMixin, Base):
    def __repr__(self):
        return "<Trx(MTS='%s', Open='%f', Close='%f')>" % (
            self.MTS, self.Open, self.Close)

class Xmr(MyMixin, Base):
    def __repr__(self):
        return "<Trx(MTS='%s', Open='%f', Close='%f')>" % (
            self.MTS, self.Open, self.Close)

class Ada(MyMixin, Base):
    def __repr__(self):
        return "<Trx(MTS='%s', Open='%f', Close='%f')>" % (
            self.MTS, self.Open, self.Close)

class Xvg(MyMixin, Base):
    def __repr__(self):
        return "<Trx(MTS='%s', Open='%f', Close='%f')>" % (
            self.MTS, self.Open, self.Close)

class Xem(MyMixin, Base):
    def __repr__(self):
        return "<Trx(MTS='%s', Open='%f', Close='%f')>" % (
            self.MTS, self.Open, self.Close)

class Ven(MyMixin, Base):
    def __repr__(self):
        return "<Trx(MTS='%s', Open='%f', Close='%f')>" % (
            self.MTS, self.Open, self.Close)

class Bnb(MyMixin, Base):
    def __repr__(self):
        return "<Trx(MTS='%s', Open='%f', Close='%f')>" % (
            self.MTS, self.Open, self.Close)

class Bcn(MyMixin, Base):
    def __repr__(self):
        return "<Trx(MTS='%s', Open='%f', Close='%f')>" % (
            self.MTS, self.Open, self.Close)

class Icx(MyMixin, Base):
    def __repr__(self):
        return "<Trx(MTS='%s', Open='%f', Close='%f')>" % (
            self.MTS, self.Open, self.Close)

class Lsk(MyMixin, Base):
    def __repr__(self):
        return "<Trx(MTS='%s', Open='%f', Close='%f')>" % (
            self.MTS, self.Open, self.Close)

class Zil(MyMixin, Base):
    def __repr__(self):
        return "<Trx(MTS='%s', Open='%f', Close='%f')>" % (
            self.MTS, self.Open, self.Close)

class Ont(MyMixin, Base):
    def __repr__(self):
        return "<Trx(MTS='%s', Open='%f', Close='%f')>" % (
            self.MTS, self.Open, self.Close)

class Ae(MyMixin, Base):
    def __repr__(self):
        return "<Trx(MTS='%s', Open='%f', Close='%f')>" % (
            self.MTS, self.Open, self.Close)

class Zrx(MyMixin, Base):
    def __repr__(self):
        return "<Trx(MTS='%s', Open='%f', Close='%f')>" % (
            self.MTS, self.Open, self.Close)

class Dcr(MyMixin, Base):
    def __repr__(self):
        return "<Trx(MTS='%s', Open='%f', Close='%f')>" % (
            self.MTS, self.Open, self.Close)

class Nano(MyMixin, Base):
    def __repr__(self):
        return "<Trx(MTS='%s', Open='%f', Close='%f')>" % (
            self.MTS, self.Open, self.Close)

class Waves(MyMixin, Base):
    def __repr__(self):
        return "<Trx(MTS='%s', Open='%f', Close='%f')>" % (
            self.MTS, self.Open, self.Close)

class Xrp(MyMixin, Base):
    def __repr__(self):
        return "<Trx(MTS='%s', Open='%f', Close='%f')>" % (
            self.MTS, self.Open, self.Close)

class Zec(MyMixin, Base):
    def __repr__(self):
        return "<Trx(MTS='%s', Open='%f', Close='%f')>" % (
            self.MTS, self.Open, self.Close)

class Elf(MyMixin, Base):
    def __repr__(self):
        return "<Trx(MTS='%s', Open='%f', Close='%f')>" % (
            self.MTS, self.Open, self.Close)

class Steem(MyMixin, Base):
    def __repr__(self):
        return "<Trx(MTS='%s', Open='%f', Close='%f')>" % (
            self.MTS, self.Open, self.Close)

class Mana(MyMixin, Base):
    def __repr__(self):
        return "<Trx(MTS='%s', Open='%f', Close='%f')>" % (
            self.MTS, self.Open, self.Close)


CryptoCompare_DB_Tables = {
    'avt': Avt,
    'ada': Ada,
    'xvg': Xvg,
    'xem': Xem,
    'ven': Ven,
    'bnb': Bnb,
    'bcn': Bcn,
    'icx': Icx,
    'lsk': Lsk,
    'zil': Zil,
    'ont': Ont,
    'ae': Ae,
    'zrx': Zrx,
    'dcr': Dcr,
    'nano': Nano,
    'waves': Waves,
    'steem': Steem,
    'rcn': Rcn,
    'rlc': Rlc,
    'elf': Elf,
    'mana': Mana
}

DB_Tables = {
    'bch': Bch,
    'btc': Btc,
    'btg': Btg,
    'dsh': Dsh,
    'eos': Eos,
    'etc': Etc,
    'eth': Eth,
    'fun': Fun,
    'gnt': Gnt,
    'iot': Iot,
    'ltc': Ltc,
    'neo': Neo,
    'omg': Omg,
    'qsh': Qsh,
    'qtm': Qtm,
    'san': San,
    'spk': Spk,
    'trx': Trx,
    'xlm': Xlm,
    'xmr': Xmr,
    'xrp': Xrp,
    'zec': Zec
}

def all_DB_tables():
    all_tables = {}
    for table in [CryptoCompare_DB_Tables, DB_Tables]:
        all_tables.update(table)

    return all_tables

