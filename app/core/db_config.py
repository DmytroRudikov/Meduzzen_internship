import os
import databases
import asyncpg
import aioredis
import redis
from dotenv import load_dotenv
from pydantic import BaseSettings


class Settings(BaseSettings):
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    TESTING: bool


settings = Settings()

load_dotenv()

r = redis.from_url(os.getenv("REDIS_URI"))

print(f'before - {os.getenv("TESTING")}')
if os.getenv("TESTING"):
    print(f'True - {os.getenv("TESTING")}')
    database = databases.Database(f"postgresql+asyncpg://postgres:passtest@localhost:5433/fastapipet", force_rollback=True)
else:
    print(f'False - {os.getenv("TESTING")}')
    database = databases.Database(f"postgresql+asyncpg://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}")

print(f'after - {os.getenv("TESTING")}')
print(database.url)

def get_sql_db() -> databases.Database:
    return database


def get_redis_db():
    return r
