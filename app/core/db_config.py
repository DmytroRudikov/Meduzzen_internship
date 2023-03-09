import os
import databases
import asyncpg
import aioredis
import redis
from dotenv import load_dotenv
from sqlalchemy.ext.declarative import declarative_base

load_dotenv()

db_uri = f"postgresql+asyncpg://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
db_url_test = f"postgresql+asyncpg://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD_TEST')}@{os.getenv('POSTGRES_HOST_TEST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"

db = databases.Database(db_uri)
r = redis.from_url(os.getenv("REDIS_URI"))

Base = declarative_base()


def get_sql_db():
    return db


def get_redis_db():
    return r
