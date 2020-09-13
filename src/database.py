from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from src import settings
from sqlalchemy import MetaData

meta = MetaData()

SQLALCHEMY_DATABASE_URL = settings.config.DATABASE_URL

engine = create_engine(SQLALCHEMY_DATABASE_URL)

DatabaseSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)

DatabaseBase = declarative_base()


def get_db():
    db = DatabaseSession()
    try:
        yield db
    finally:
        db.close()
