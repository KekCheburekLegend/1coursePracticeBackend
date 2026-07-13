from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
import os

DB_URL = os.getenv("DB_URL")

engine = create_engine(DB_URL,
                       pool_size=150,
                       max_overflow=350,
                       pool_timeout=60,
                       pool_pre_ping=True,
                       pool_recycle=1800,
                       pool_use_lifo=True,
                       pool_reset_on_return="rollback",
                       )

session_local = sessionmaker(autoflush=False, autocommit=False, bind=engine)

Base = declarative_base()


def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()
