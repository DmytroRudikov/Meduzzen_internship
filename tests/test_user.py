from httpx import AsyncClient
import pytest


@pytest.mark.asyncio
async def test_get_users(ac: AsyncClient):
    response = await ac.get("/users")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_bad_create_user_not_passord(ac: AsyncClient):
    payload = {
      "password": "",
      "password_check": "",
      "email": "test@test.test",
      "first_name": "test",
      "last_name": "1"
    }
    response = await ac.post("/user", json=payload)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_bad_create_user_low_passord(ac: AsyncClient):
    payload = {
      "password": "tet",
      "password_check": "tet",
      "email": "test@test.test",
      "first_name": "test",
      "last_name": "1",
    }
    response = await ac.post("/user", json=payload)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_bad_create_user_dont_match(ac: AsyncClient):
    payload = {
      "password": "test",
      "password_check": "tess",
      "email": "test@test.test",
      "first_name": "test",
      "last_name": "1"
    }
    response = await ac.post("/user", json=payload)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_bad_create_user_no_valid_email(ac: AsyncClient):
    payload = {
      "password": "test",
      "password_check": "tess",
      "email": "test",
      "first_name": "test",
      "last_name": "1"
    }
    response = await ac.post("/user", json=payload)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_user_one(ac: AsyncClient):
    payload = {
      "password": "testt",
      "password_check": "testt",
      "email": "test1@test.com",
      "first_name": "test",
      "last_name": "1"
    }
    response = await ac.post("/user", json=payload)
    assert response.status_code == 200
    assert response.json().get("id") == 1


@pytest.mark.asyncio
async def test_create_user_error(ac: AsyncClient):
    payload = {
      "password": "testt",
      "password_check": "testt",
      "email": "test1@test.com",
      "first_name": "test",
      "last_name": "2"
    }
    response = await ac.post("/user", json=payload)
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_create_user_two(ac: AsyncClient):
    payload = {
      "password": "testt",
      "password_check": "testt",
      "email": "test2@test.com",
      "first_name": "test",
      "last_name": "2"
    }
    response = await ac.post("/user", json=payload)
    assert response.status_code == 200
    assert response.json().get("id") == 2


@pytest.mark.asyncio
async def test_create_user_three(ac: AsyncClient):
    payload = {
      "password": "testt",
      "password_check": "testt",
      "email": "test3@test.com",
      "first_name": "test",
      "last_name": "3"
    }
    response = await ac.post("/user", json=payload)
    assert response.status_code == 200
    assert response.json().get("id") == 3


@pytest.mark.asyncio
async def test_get_users_list(ac: AsyncClient):
    response = await ac.get("/users")
    assert response.status_code == 200
    assert len(response.json()) == 3


@pytest.mark.asyncio
async def test_get_user_by_id(ac: AsyncClient):
    response = await ac.get("/user?user_id=1")
    assert response.status_code == 200
    assert response.json().get("id") == 1
    assert response.json().get("email") == 'test1@test.com'
    assert response.json().get("first_name") == 'test'
    assert response.json().get("last_name") == '1'


@pytest.mark.asyncio
async def test_bad_get_user_by_id(ac: AsyncClient):
    response = await ac.get("/user?user_id=4")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_user_one(ac: AsyncClient):
    payload = {
      "first_name": "test1",
      "last_name": "NEW"
    }
    response = await ac.put("/user?user_id=1", json=payload)
    assert response.status_code == 200
    assert response.json().get("id") == 1


@pytest.mark.asyncio
async def test_get_user_by_id_updates(ac: AsyncClient):
    response = await ac.get("/user?user_id=1")
    assert response.status_code == 200
    assert response.json().get("id") == 1
    assert response.json().get("email") == 'test1@test.com'
    assert response.json().get("first_name") == 'test1'
    assert response.json().get("last_name") == 'NEW'


@pytest.mark.asyncio
async def test_update_user_not_exist(ac: AsyncClient):
    payload = {
      "first_name": "test1NEW"
    }
    response = await ac.put("/user?user_id=4", json=payload)
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_user_one(ac: AsyncClient):
    response = await ac.delete("/user?user_id=1")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_users_list_after_delete(ac: AsyncClient):
    response = await ac.get("/users")
    assert response.status_code == 200
    assert len(response.json()) == 2