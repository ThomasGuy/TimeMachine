import logging
from datetime import datetime

# Third party imports
from flask_sqlalchemy_session import current_session
from sqlalchemy import Table, Column, DateTime, Float, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# package imports
from .models import Base

log = logging.getLogger(__name__)



class User(UserMixin, Base):
    __tablename__='users'

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

