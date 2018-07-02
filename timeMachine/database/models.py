from datetime import datetime

# Third party imports
from sqlalchemy import Column, DateTime, Float, String, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from flask_sqlalchemy_session import current_session as cs
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# TimaMachine imports
from timeMachine.server import login


Base = declarative_base()


class User(UserMixin, Base):
    __tablename__ = 'users'

    id = Column(Integer(), primary_key=True)
    username = Column(String(64), index=True, unique=True)
    email = Column(String(120), index=True, unique=True)
    password_hash = Column(String(128))
    # profile = relationship('Profile', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Profile(Base):
    __tablename__= 'profiles'

    profile_id = Column(Integer, primary_key=True)
    body = Column(String(255))
    user_id = Column(Integer(), ForeignKey('users.id'))

    # user = relationship("User", backref=backref('profiles', order_by=profile_id))

    def __repr__(self):
        return '<Profile {}>'.format(self.body)



@login.user_loader
def load_user(id):
    return cs.query(User).get(int(id))


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

    def __repr__(self):
        return "<%s (MTS='%s', Open='%f', Close='%f')>" % (
            self.__tablename__, self.MTS, self.Open, self.Close)


class Avt(MyMixin, Base):
    pass
    
class Bch(MyMixin, Base):
    pass

class Btc(MyMixin, Base):
    pass

class Btg(MyMixin, Base):
    pass
            
class Dsh(MyMixin, Base):
    pass
            
class Eos(MyMixin, Base):
    pass
            
class Etc(MyMixin, Base):
    pass

class Eth(MyMixin, Base):
    pass

class Fun(MyMixin, Base):
    pass

class Gnt(MyMixin, Base):
    pass

class Iot(MyMixin, Base):
    pass

class Ltc(MyMixin, Base):
    pass

class Neo(MyMixin, Base):
    pass

class Qsh(MyMixin, Base):
    pass

class Qtm(MyMixin, Base):
    pass

class Omg(MyMixin, Base):
    pass

class Rcn(MyMixin, Base):
    pass

class Rlc(MyMixin, Base):
    pass

class San(MyMixin, Base):
    pass

class Spk(MyMixin, Base):
    pass

class Trx(MyMixin, Base):
    pass

class Xlm(MyMixin, Base):
    pass

class Xmr(MyMixin, Base):
    pass

class Ada(MyMixin, Base):
    pass

class Xvg(MyMixin, Base):
    pass

class Xem(MyMixin, Base):
    pass

class Ven(MyMixin, Base):
    pass

class Bnb(MyMixin, Base):
    pass

class Bcn(MyMixin, Base):
    pass

class Icx(MyMixin, Base):
    pass

class Lsk(MyMixin, Base):
    pass

class Zil(MyMixin, Base):
    pass

class Ont(MyMixin, Base):
    pass

class Ae(MyMixin, Base):
    pass

class Zrx(MyMixin, Base):
    pass

class Dcr(MyMixin, Base):
    pass

class Nano(MyMixin, Base):
    pass

class Waves(MyMixin, Base):
    pass

class Xrp(MyMixin, Base):
    pass

class Zec(MyMixin, Base):
    pass

class Elf(MyMixin, Base):
    pass

class Steem(MyMixin, Base):
    pass

class Mana(MyMixin, Base):
    pass


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
    return {**CryptoCompare_DB_Tables, **DB_Tables}