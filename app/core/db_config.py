import os
import databases
import asyncpg
import aioredis
from dotenv import load_dotenv
from pydantic import BaseSettings


class Settings(BaseSettings):
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    TESTING: bool


settings = Settings()

load_dotenv()

r = aioredis.from_url(os.getenv("REDIS_URI"))

if settings.TESTING:
    database = databases.Database(f"postgresql+asyncpg://postgres:passtest@localhost:5433/fastapipet", force_rollback=True)
else:
    database = databases.Database(f"postgresql+asyncpg://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}")


def get_sql_db() -> databases.Database:
    return database


def get_redis_db():
    return r
