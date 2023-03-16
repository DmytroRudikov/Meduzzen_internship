import asyncio
import pytest
import pytest_asyncio

from typing import AsyncGenerator
from starlette.testclient import TestClient
from databases import Database
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.pool import NullPool
from httpx import AsyncClient

#import your app
from app.main import app
#import your metadata
from app.db.models import Base
#import your test database
from app.core.db_config import database as test_db

engine_test = create_async_engine(str(test_db.url), poolclass=NullPool)


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def test_app():
    client = TestClient(app)
    yield client


@pytest_asyncio.fixture(autouse=True, scope='session')
async def prepare_database():
    await test_db.connect()
    print("@@@@@1111@@@@")
    print(test_db.is_connected)
    print(test_db.connection())
    print(test_db.url)
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    print("@@@@@22222@@@@")
    print(test_db.connection())
    await test_db.disconnect()
    print(test_db.is_connected)
    print(test_db.url)
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest_asyncio.fixture(scope='session')
async def login_user(ac: AsyncClient, users_tokens):
    async def __send_request(user_email: str, user_password: str):
        payload = {
            "email": user_email,
            "password": user_password,
        }
        response = await ac.post("/auth/login", json=payload)
        if response.status_code != 200:
            return response
        user_token = response.json().get('access_token')
        users_tokens[user_email] = user_token
        return response

    return __send_request


@pytest_asyncio.fixture(scope='session')
def users_tokens():
    tokens_store = dict()
    return tokens_store
