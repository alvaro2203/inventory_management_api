from sqlmodel import Session, create_engine
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
from contextlib import contextmanager
import os

load_dotenv()

DB_URL = os.getenv("DB_URL")
if not DB_URL:
    raise ValueError("The local environment DB_URL is not defined.")

engine = create_engine(
    DB_URL, 
    pool_pre_ping=True,
    pool_recycle=3600,
    echo=False
)

Base = declarative_base()

def get_db():
    """
        Create a DB session, use it and ensure to close it.
    """
    with Session(engine) as db: 
        yield db

@contextmanager
def get_db_context():
    """
        Provides a DB session using the Context Manager pattern.
    """
    with Session(engine) as db: 
        yield db