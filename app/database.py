from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

SQLALCHEMY_DATABASE_URL=os.getenv("DATABASE_URI")

engine = create_engine(SQLALCHEMY_DATABASE_URL)
Session_Local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = Session_Local()
    try:
        yield db
    finally:
        db.close()