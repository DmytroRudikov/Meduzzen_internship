import os
import databases
import asyncpg
import aioredis
import redis
from dotenv import load_dotenv

load_dotenv()

db_uri = f"postgresql+asyncpg://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
db = databases.Database(db_uri)
r = redis.from_url(os.getenv("REDIS_URI"))


def get_sql_db():
    return db


def get_redis_db():
    return r
