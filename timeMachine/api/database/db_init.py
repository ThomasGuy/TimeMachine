from datetime import datetime

# Third party imports
from sqlalchemy import Table, Column, DateTime, Float, String, Integer, create_engine
from sqlalchemy.ext.declarative import declarative_base, declared_attr

# TimaMachine imports
from ..initialize import db_name


Base = declarative_base()
engine = create_engine(db_name, echo=False)


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

class Xrp(MyMixin, Base):
    def __repr__(self):
        return "<Xrp(MTS='%s', Open='%f', Close='%f')>" % (
            self.MTS, self.Open, self.Close)

class Zec(MyMixin, Base):
    def __repr__(self):
        return "<Zec(MTS='%s', Open='%f', Close='%f')>" % (
            self.MTS, self.Open, self.Close)


class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer(), primary_key=True)
    username = Column(String(15), nullable=False, unique=True)
    email_address = Column(String(255), nullable=False)
    password = Column(String(25), nullable=False)
    created_on = Column(DateTime(), default=datetime.now)
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return "User(username='{self.username}', " \
            "email_address='{self.email_address}', ".format(self=self)


Base.metadata.create_all(engine)

DB_Tables = {
    'avt': Avt,
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
    'rcn': Rcn,
    'rlc': Rlc,
    'san': San,
    'spk': Spk,
    'trx': Trx,
    'xlm': Xlm,
    'xmr': Xmr,
    'xrp': Xrp,
    'zec': Zec
}
