# Third party imports
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from timeMachine.config import Config

# package imports
# from timeMachine.database import models
from .models import Base


engine = create_engine(Config.DATABASE_URI, echo=False)
Base.metadata.create_all(engine)

session_factory = sessionmaker(bind=engine)
