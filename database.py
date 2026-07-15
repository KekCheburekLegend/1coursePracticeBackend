from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

DB_URL = os.getenv("DB_URL")

engine = create_async_engine(DB_URL,
                       pool_size=20,
                       max_overflow=70,
                       pool_timeout=60,
                       pool_pre_ping=True,
                       pool_recycle=1800,
                       pool_use_lifo=True,
                       pool_reset_on_return="rollback",
                       )

session_local = async_sessionmaker(engine, autocommit=False, autoflush=False,)

Base = declarative_base()


async def get_db():
    db = session_local()
    try:
        yield db
    finally:
        await db.close()
