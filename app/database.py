
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from settings import DB_URL

def get_db_context():
    try:
        db = LocalSession()
        yield db
    finally:
        db.close()

engine = create_engine(DB_URL)
metadata = MetaData()

LocalSession = sessionmaker(autoflush=False, autocommit=False, bind=engine)
Base = declarative_base()