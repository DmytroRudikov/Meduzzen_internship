from httpx import AsyncClient
import pytest

# ---------- Get notification ---------- #


@pytest.mark.asyncio
async def test_get_notifications_not_auth(ac: AsyncClient, users_tokens):
    response = await ac.get('/my_notifications')
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_get_notifications_user_one_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.get('/my_notifications', headers=headers)
    assert response.status_code == 200
    assert len(response.json().get('items')) == 0


@pytest.mark.asyncio
async def test_get_notifications_user_four_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test4@test.com']}",
    }
    response = await ac.get('/my_notifications', headers=headers)
    assert response.status_code == 200
    assert len(response.json().get('items')) == 2
    assert response.json().get("items")[0].get("company_id") == 4
    assert response.json().get("items")[0].get("user_id") == 4
    assert response.json().get("items")[0].get("quiz_record_id") == 2
    assert response.json().get("items")[0].get("status") == "unread"
    assert response.json().get("items")[1].get("company_id") == 4
    assert response.json().get("items")[1].get("user_id") == 4
    assert response.json().get("items")[1].get("quiz_record_id") == 3
    assert response.json().get("items")[1].get("status") == "unread"


@pytest.mark.asyncio
async def test_get_notifications_user_two_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/my_notifications', headers=headers)
    assert response.status_code == 200
    assert len(response.json().get('items')) == 2
    assert response.json().get("items")[0].get("company_id") == 4
    assert response.json().get("items")[0].get("user_id") == 2
    assert response.json().get("items")[0].get("quiz_record_id") == 2
    assert response.json().get("items")[0].get("status") == "unread"
    assert response.json().get("items")[1].get("company_id") == 4
    assert response.json().get("items")[1].get("user_id") == 2
    assert response.json().get("items")[1].get("quiz_record_id") == 3
    assert response.json().get("items")[1].get("status") == "unread"


@pytest.mark.asyncio
async def test_get_notifications_user_six_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test6@test.com']}",
    }
    response = await ac.get('/my_notifications', headers=headers)
    assert response.status_code == 200
    assert len(response.json().get('items')) == 2
    assert response.json().get("items")[0].get("company_id") == 4
    assert response.json().get("items")[0].get("user_id") == 6
    assert response.json().get("items")[0].get("quiz_record_id") == 2
    assert response.json().get("items")[0].get("status") == "unread"
    assert response.json().get("items")[1].get("company_id") == 4
    assert response.json().get("items")[1].get("user_id") == 6
    assert response.json().get("items")[1].get("quiz_record_id") == 3
    assert response.json().get("items")[1].get("status") == "unread"


# ---------- Update notification ---------- #

@pytest.mark.asyncio
async def test_update_notification_not_auth(ac: AsyncClient):
    response = await ac.put('/my_notifications/1/read')
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_update_notification_user_4_not_allowed(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.put('/my_notifications/1/read', headers=headers)
    assert response.status_code == 403
    assert response.json().get('detail') == "You are allowed to change status of only unread notifications that belong to you"


@pytest.mark.asyncio
async def test_update_notification_5_user_4_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test4@test.com']}",
    }
    response = await ac.put('/my_notifications/5/read', headers=headers)
    assert response.status_code == 200
    assert response.json().get('detail') == "success"


@pytest.mark.asyncio
async def test_update_notification_8_user_4_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test4@test.com']}",
    }
    response = await ac.put('/my_notifications/8/read', headers=headers)
    assert response.status_code == 200
    assert response.json().get('detail') == "success"


@pytest.mark.asyncio
async def test_update_notification_7_user_6_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test6@test.com']}",
    }
    response = await ac.put('/my_notifications/7/read', headers=headers)
    assert response.status_code == 200
    assert response.json().get('detail') == "success"


@pytest.mark.asyncio
async def test_get_upd_notifications_user_six_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test6@test.com']}",
    }
    response = await ac.get('/my_notifications', headers=headers)
    assert response.status_code == 200
    assert len(response.json().get('items')) == 1
    assert response.json().get("items")[0].get("company_id") == 4
    assert response.json().get("items")[0].get("user_id") == 6
    assert response.json().get("items")[0].get("quiz_record_id") == 2
    assert response.json().get("items")[0].get("status") == "unread"
    assert response.json().get("items")[0].get("notification_id") == 4


@pytest.mark.asyncio
async def test_get_upd_notifications_user_four_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test4@test.com']}",
    }
    response = await ac.get('/my_notifications', headers=headers)
    assert response.status_code == 200
    assert len(response.json().get('items')) == 0


@pytest.mark.asyncio
async def test_get_upd_notifications_user_two_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/my_notifications', headers=headers)
    assert response.status_code == 200
    assert len(response.json().get('items')) == 2
    assert response.json().get("items")[0].get("company_id") == 4
    assert response.json().get("items")[0].get("user_id") == 2
    assert response.json().get("items")[0].get("quiz_record_id") == 2
    assert response.json().get("items")[0].get("status") == "unread"
    assert response.json().get("items")[1].get("company_id") == 4
    assert response.json().get("items")[1].get("user_id") == 2
    assert response.json().get("items")[1].get("quiz_record_id") == 3
    assert response.json().get("items")[1].get("status") == "unread"
