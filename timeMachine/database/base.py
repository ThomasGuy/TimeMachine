# Third party imports
import pymysql
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from timeMachine.config import Config

# package imports
from .models import Base, BaseModel


engine = create_engine(Config.DATABASE_URI, pool_recycle=3000, echo=False, pool_pre_ping=True)
Base.metadata.create_all(engine)

session_factory = sessionmaker(bind=engine)
