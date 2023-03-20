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


@pytest.mark.asyncio
async def test_bad_login_try(ac: AsyncClient):
    payload = {
        "email": "test2@test.com",
        "password": "tess",
    }
    response = await ac.post("/auth/login", json=payload)
    assert response.status_code == 401
    assert response.json().get('detail') == 'Incorrect username or password'


@pytest.mark.asyncio
async def test_login_try(ac: AsyncClient, login_user):
    response = await login_user("test2@test.com", "testt")
    assert response.status_code == 200
    assert response.json().get('token_type') == 'Bearer'


@pytest.mark.asyncio
async def test_auth_me(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}"
    }
    response = await ac.get("/auth/me", headers=headers)
    assert response.status_code == 200
    assert response.json().get('first_name') == "test"
    assert response.json().get('last_name') == "2"
    assert response.json().get('email') == "test2@test.com"
    assert response.json().get('id') == 2


@pytest.mark.asyncio
async def test_bad_auth_me(ac: AsyncClient):
    headers = {
        "Authorization": f"Bearer sdffaf.afdsg.rtrwtrete",
    }
    response = await ac.get("/auth/me", headers=headers)
    assert response.status_code == 401


# =====================================================


@pytest.mark.asyncio
async def test_get_users_list_auth(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}"
    }
    response = await ac.get("/users", headers=headers)
    assert response.status_code == 200
    assert len(response.json().get("users")) == 3


@pytest.mark.asyncio
async def test_get_users_list_unauth(ac: AsyncClient):
    response = await ac.get("/users")
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_get_user_by_id_auth(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}"
    }
    response = await ac.get("/user?user_id=1", headers=headers)
    assert response.status_code == 200
    assert response.json().get("id") == 1
    assert response.json().get("email") == 'test1@test.com'
    assert response.json().get("first_name") == 'test'
    assert response.json().get('last_name') == "1"


async def test_get_user_by_id_unauth(ac: AsyncClient):
    response = await ac.get("/user?user_id=1")
    assert response.status_code == 403


async def test_bad_get_user_by_id_auth(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}"
    }
    response = await ac.get("/user?user_id=4", headers=headers)
    assert response.status_code == 404


async def test_update_user_one_bad(ac: AsyncClient, users_tokens):
    payload = {
      "first_name": "test1",
      "last_name": "NEW"
    }
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}"
    }
    response = await ac.put("/user?user_id=1", json=payload, headers=headers)
    assert response.status_code == 403
    assert response.json().get("detail") == "It's not your account"


async def test_update_user_one_good(ac: AsyncClient, users_tokens):
    payload = {
      "first_name": "test2",
      "last_name": "NEW"
    }
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}"
    }
    response = await ac.put("/user?user_id=2", json=payload, headers=headers)
    assert response.status_code == 200
    assert response.json().get("id") == 2


async def test_get_user_by_id_updates_auth(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}"
    }
    response = await ac.get("/user?user_id=2", headers=headers)
    assert response.status_code == 200
    assert response.json().get("id") == 2
    assert response.json().get("email") == 'test2@test.com'
    assert response.json().get("last_name") == 'test2'
    assert response.json().get("first_name") == 'NEW'


async def test_delete_user_one_bad(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}"
    }
    response = await ac.delete("/user?user_id=1", headers=headers)
    assert response.status_code == 403
    assert response.json().get("detail") == "It's not your account"


async def test_delete_user_one_good(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}"
    }
    response = await ac.delete("/user?user_id=2", headers=headers)
    assert response.status_code == 200


async def test_login_user_one(ac: AsyncClient, login_user):
    response = await login_user("test1@test.com", "testt")
    assert response.status_code == 200
    assert response.json().get('token_type') == 'Bearer'


async def test_get_users_list_after_delete_auth(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}"
    }
    response = await ac.get("/users", headers=headers)
    assert response.status_code == 200
    assert len(response.json().get("users")) == 2
