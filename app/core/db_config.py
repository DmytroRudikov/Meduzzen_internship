import os
import databases
import asyncpg
import aioredis
import redis
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.exc import InvalidRequestError

load_dotenv()

db_uri = f"postgresql+asyncpg://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
db_url_test = f"postgresql+asyncpg://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD_TEST')}@{os.getenv('POSTGRES_HOST_TEST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
db = databases.Database(db_uri)
r = redis.from_url(os.getenv("REDIS_URI"))

engine = create_async_engine(db_uri, echo=True)
async_session = sessionmaker(bind=engine, autocommit=False, autoflush=False, expire_on_commit=False, class_=AsyncSession)
Base = declarative_base()


def get_sql_db():
    return db


def get_redis_db():
    return r


async def get_session():
    async with async_session.begin() as session:
        yield session
