from httpx import AsyncClient
import pytest


@pytest.mark.asyncio
async def test_bad_create_user_not_password(ac: AsyncClient):
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
async def test_bad_create_user_low_password(ac: AsyncClient):
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
      "password": "test1",
      "password_check": "test1",
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
      "password": "test2",
      "password_check": "test2",
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
      "password": "test3",
      "password_check": "test3",
      "email": "test3@test.com",
      "first_name": "test",
      "last_name": "3"
    }
    response = await ac.post("/user", json=payload)
    assert response.status_code == 200
    assert response.json().get("id") == 3


@pytest.mark.asyncio
async def test_create_user_four(ac: AsyncClient):
    payload = {
        "password": "test4",
        "password_check": "test4",
        "email": "test4@test.com",
        "first_name": "test",
        "last_name": "4",
    }
    response = await ac.post("/user", json=payload)
    assert response.status_code == 200
    assert response.json().get("id") == 4


@pytest.mark.asyncio
async def test_create_user_five(ac: AsyncClient):
    payload = {
        "password": "test5",
        "password_check": "test5",
        "email": "test5@test.com",
        "first_name": "test",
        "last_name": "5",
    }
    response = await ac.post("/user", json=payload)
    assert response.status_code == 200
    assert response.json().get("id") == 5


# =================================


@pytest.mark.asyncio
async def test_bad_try_login(ac: AsyncClient, login_user):
    response = await login_user("test2@test.com", "test_bad")
    assert response.status_code == 401
    assert response.json().get('detail') == 'Incorrect username or password'


@pytest.mark.asyncio
async def test_try_login_one(ac: AsyncClient, login_user):
    response = await login_user("test1@test.com", "test1")
    assert response.status_code == 200
    assert response.json().get('token_type') == 'Bearer'


@pytest.mark.asyncio
async def test_try_login_two(ac: AsyncClient, login_user):
    response = await login_user("test2@test.com", "test2")
    assert response.status_code == 200
    assert response.json().get('token_type') == 'Bearer'


@pytest.mark.asyncio
async def test_try_login_three(ac: AsyncClient, login_user):
    response = await login_user("test3@test.com", "test3")
    assert response.status_code == 200
    assert response.json().get('token_type') == 'Bearer'


@pytest.mark.asyncio
async def test_try_login_four(ac: AsyncClient, login_user):
    response = await login_user("test4@test.com", "test4")
    assert response.status_code == 200
    assert response.json().get('token_type') == 'Bearer'


@pytest.mark.asyncio
async def test_try_login_five(ac: AsyncClient, login_user):
    response = await login_user("test5@test.com", "test5")
    assert response.status_code == 200
    assert response.json().get('token_type') == 'Bearer'


@pytest.mark.asyncio
async def test_auth_me_one(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.get("/auth/me", headers=headers)
    assert response.status_code == 200
    assert response.json().get('first_name') == "test"
    assert response.json().get('last_name') == "1"
    assert response.json().get('email') == "test1@test.com"
    assert response.json().get('id') == 1
    assert response.json().get('password') is None


@pytest.mark.asyncio
async def test_auth_me_two(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get("/auth/me", headers=headers)
    assert response.status_code == 200
    assert response.json().get('first_name') == "test"
    assert response.json().get('last_name') == "2"
    assert response.json().get('email') == "test2@test.com"
    assert response.json().get('id') == 2
    assert response.json().get('password') is None


@pytest.mark.asyncio
async def test_bad_auth_me(ac: AsyncClient):
    headers = {
        "Authorization": "Bearer retretwetrt.rqwryerytwetrty",
    }
    response = await ac.get("/auth/me", headers=headers)
    assert response.status_code == 401

# =====================================================


@pytest.mark.asyncio
async def test_get_users_list(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.get("/users", headers=headers)
    assert response.status_code == 200
    assert len(response.json().get("items")) == 5


@pytest.mark.asyncio
async def test_get_users_list_unauth(ac: AsyncClient):
    response = await ac.get("/users")
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_get_user_by_id(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.get("/user/2", headers=headers)
    assert response.status_code == 200
    assert response.json().get('first_name') == "test"
    assert response.json().get('last_name') == "2"
    assert response.json().get('email') == "test2@test.com"
    assert response.json().get('id') == 2
    assert response.json().get('password') is None


@pytest.mark.asyncio
async def test_get_user_by_id_unauth(ac: AsyncClient):
    response = await ac.get("/user/2")
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_bad_get_user_by_id__not_found(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.get("/user/6", headers=headers)
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_bad_update_user_one__not_your_acc(ac: AsyncClient, users_tokens):
    payload = {
        "first_name": "test1NEW",
    }
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.put("/user/2", json=payload, headers=headers)
    assert response.status_code == 403
    assert response.json().get("detail") == "It's not your account"


@pytest.mark.asyncio
async def test_update_user_one(ac: AsyncClient, users_tokens):
    payload = {
        "first_name": "test1NEW",
    }
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.put("/user/1", json=payload, headers=headers)
    assert response.status_code == 200
    assert response.json().get("id") == 1


@pytest.mark.asyncio
async def test_get_user_by_id_updated(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.get("/user/1", headers=headers)
    assert response.json().get('first_name') == "test1NEW"
    assert response.json().get('last_name') == "1"
    assert response.json().get('email') == "test1@test.com"
    assert response.json().get('id') == 1
    assert response.json().get('password') is None


@pytest.mark.asyncio
async def test_bad_delete_user_five__not_your_acc(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.delete("/user/5", headers=headers)
    assert response.status_code == 403
    assert response.json().get("detail") == "It's not your account"


@pytest.mark.asyncio
async def test_delete_user_five(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test5@test.com']}",
    }
    response = await ac.delete("/user/5", headers=headers)
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_users_list_after_delete(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.get("/users", headers=headers)
    assert response.status_code == 200
    assert len(response.json().get("items")) == 4
