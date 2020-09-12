from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from src.main import config

SQLALCHEMY_DATABASE_URL = config.DATABASE_URL

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

DatabaseSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)

DatabaseBase = declarative_base()