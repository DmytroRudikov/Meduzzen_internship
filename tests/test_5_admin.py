from httpx import AsyncClient
import pytest


@pytest.mark.asyncio
async def test_create_admin_not_auth(ac: AsyncClient):
    payload = {
        "company_member_id": 1
    }
    response = await ac.post('/company/4/admin', json=payload)
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_create_admin_company_not_found(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    payload = {
        "company_member_id": 2,
    }
    response = await ac.post('/company/100/admin', headers=headers, json=payload)
    assert response.status_code == 404
    assert response.json().get('detail') == "Company does not exist"


@pytest.mark.asyncio
async def test_create_admin_user_not_found(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    payload = {
        "company_member_id": 100,
    }
    response = await ac.post('/company/4/admin', headers=headers, json=payload)
    assert response.status_code == 404, response.json()
    assert response.json().get('detail') == "Company member with id 100 not found"


@pytest.mark.asyncio
async def test_create_admin_not_owner(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    payload = {
        "company_member_id": 2,
    }
    response = await ac.post('/company/4/admin', headers=headers, json=payload)
    assert response.status_code == 403
    assert response.json().get('detail') == "It's not your company"


@pytest.mark.asyncio
async def test_create_admin_two_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    payload = {
        "company_member_id": 2,
    }
    response = await ac.post('/company/4/admin', headers=headers, json=payload)
    assert response.status_code == 200
    assert response.json().get('detail') == 'success'


@pytest.mark.asyncio
async def test_create_admin_three_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    payload = {
        "company_member_id": 3,
    }
    response = await ac.post('/company/4/admin', headers=headers, json=payload)
    assert response.status_code == 200
    assert response.json().get('detail') == 'success'


# admin-list

@pytest.mark.asyncio
async def test_admin_list_not_auth(ac: AsyncClient):
    response = await ac.get('/company/4/admins')
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_admin_list_not_found(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.get('/company/100/admins', headers=headers)
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_admin_list_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.get('/company/4/admins', headers=headers)
    assert response.status_code == 200
    assert len(response.json().get('items')) == 2


# admin-remove

@pytest.mark.asyncio
async def test_admin_remove_not_auth(ac: AsyncClient):
    response = await ac.delete('/company/4/admin/2')
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_admin_remove_user_not_found(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.delete('/company/4/admin/100', headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == 'Company member with id 100 not found'


@pytest.mark.asyncio
async def test_admin_remove_company_not_found(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.delete('/company/100/admin/3', headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == 'Company does not exist'


@pytest.mark.asyncio
async def test_admin_remove_not_owner(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.delete('/company/4/admin/3', headers=headers)
    assert response.status_code == 403
    assert response.json().get('detail') == "It's not your company"


@pytest.mark.asyncio
async def test_admin_remove_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }

    response = await ac.delete('/company/4/admin/2', headers=headers)
    assert response.status_code == 200
    assert response.json().get('detail') == "success"


@pytest.mark.asyncio
async def test_admin_list_success_after_remove(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.get('/company/4/admins', headers=headers)
    assert response.status_code == 200
    assert len(response.json().get('items')) == 1


@pytest.mark.asyncio
async def test_admin_list_control(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    response = await ac.get('/company/1/admins', headers=headers)
    assert response.status_code == 200
    assert len(response.json().get('items')) == 0
