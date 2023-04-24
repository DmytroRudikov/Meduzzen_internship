from httpx import AsyncClient
import pytest

# ---------- Export user results json ---------- #


@pytest.mark.asyncio
async def test_export_user_results_json_not_auth(ac: AsyncClient, users_tokens):
    response = await ac.get('/my_results/export/json')
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_export_user_4_results_json_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test4@test.com']}",
    }
    response = await ac.get('/my_results/export/json', headers=headers)
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_export_user_1_results_json_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.get('/my_results/export/json', headers=headers)
    assert response.status_code == 200


# ---------- Export user results csv ---------- #


@pytest.mark.asyncio
async def test_export_user_results_csv_not_auth(ac: AsyncClient, users_tokens):
    response = await ac.get('/my_results/export/csv')
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_export_user_4_results_csv_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test4@test.com']}",
    }
    response = await ac.get('/my_results/export/csv', headers=headers)
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_export_user_1_results_csv_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.get('/my_results/export/csv', headers=headers)
    assert response.status_code == 200


# ---------- Export company results json ---------- #


@pytest.mark.asyncio
async def test_export_company_results_json_not_auth(ac: AsyncClient, users_tokens):
    response = await ac.get('/company/4/results/export/json')
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_export_company_results_json_company_not_exists(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test4@test.com']}",
    }
    response = await ac.get('/company/40/results/export/json', headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == 'Company does not exist'


@pytest.mark.asyncio
async def test_export_results_json_comp_4_not_allowed(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test4@test.com']}",
    }
    response = await ac.get('/company/4/results/export/json', headers=headers)
    assert response.status_code == 403
    assert response.json().get('detail') == 'You are not allowed to export results'


@pytest.mark.asyncio
async def test_export_results_json_comp_4_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/company/4/results/export/json', headers=headers)
    assert response.status_code == 200


# ---------- Export company results csv ---------- #


@pytest.mark.asyncio
async def test_export_company_results_csv_not_auth(ac: AsyncClient, users_tokens):
    response = await ac.get('/company/4/results/export/csv')
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_export_company_results_csv_company_not_exists(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test4@test.com']}",
    }
    response = await ac.get('/company/40/results/export/csv', headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == 'Company does not exist'


@pytest.mark.asyncio
async def test_export_results_csv_comp_4_not_allowed(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test4@test.com']}",
    }
    response = await ac.get('/company/4/results/export/csv', headers=headers)
    assert response.status_code == 403
    assert response.json().get('detail') == 'You are not allowed to export results'


@pytest.mark.asyncio
async def test_export_results_csv_comp_4_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/company/4/results/export/csv', headers=headers)
    assert response.status_code == 200


# ---------- Export company member results json ---------- #


@pytest.mark.asyncio
async def test_export_company_member_results_json_not_auth(ac: AsyncClient, users_tokens):
    response = await ac.get('/company/4/member/4/results/export/json')
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_export_company_member_results_json_company_not_exists(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/company/40/member/4/results/export/json', headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == 'Company does not exist'


@pytest.mark.asyncio
async def test_export_company_member_results_json_mem_not_exists(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/company/4/member/40/results/export/json', headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == 'Company member with id 40 not found'


@pytest.mark.asyncio
async def test_export_company_member_results_json_comp_4_not_allowed(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test4@test.com']}",
    }
    response = await ac.get('/company/4/member/2/results/export/json', headers=headers)
    assert response.json().get('detail') == 'You are not allowed to export results'
    assert response.status_code == 403



@pytest.mark.asyncio
async def test_export_company_member_results_json_comp_4_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/company/4/member/2/results/export/json', headers=headers)
    assert response.status_code == 200


# ---------- Export company member results csv ---------- #


@pytest.mark.asyncio
async def test_export_company_member_results_csv_not_auth(ac: AsyncClient, users_tokens):
    response = await ac.get('/company/4/member/4/results/export/csv')
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_export_company_member_results_csv_company_not_exists(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/company/40/member/4/results/export/csv', headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == 'Company does not exist'


@pytest.mark.asyncio
async def test_export_company_member_results_csv_mem_not_exists(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/company/4/member/40/results/export/csv', headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == 'Company member with id 40 not found'


@pytest.mark.asyncio
async def test_export_company_member_results_csv_comp_4_not_allowed(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test4@test.com']}",
    }
    response = await ac.get('/company/4/member/2/results/export/csv', headers=headers)
    assert response.status_code == 403
    assert response.json().get('detail') == 'You are not allowed to export results'


@pytest.mark.asyncio
async def test_export_company_member_results_csv_comp_4_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/company/4/member/2/results/export/csv', headers=headers)
    assert response.status_code == 200


# ---------- Export company results for quiz specified json ---------- #


@pytest.mark.asyncio
async def test_export_company_results_quiz_1_json_not_auth(ac: AsyncClient, users_tokens):
    response = await ac.get('/company/4/quiz/1/results/export/json')
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_export_company_results_quiz_1_json_company_not_exists(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/company/40/quiz/1/results/export/json', headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == 'Company does not exist'


@pytest.mark.asyncio
async def test_export_company_4_results_quiz_10_json_quiz_not_exists(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/company/4/quiz/10/results/export/json', headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == 'Quiz not found'


@pytest.mark.asyncio
async def test_export_company_4_results_quiz_1_json_comp_4_not_allowed(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test4@test.com']}",
    }
    response = await ac.get('/company/4/quiz/1/results/export/json', headers=headers)
    assert response.status_code == 403
    assert response.json().get('detail') == 'You are not allowed to export results'


@pytest.mark.asyncio
async def test_export_company_4_results_quiz_1_json_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test6@test.com']}",
    }
    response = await ac.get('/company/4/quiz/1/results/export/json', headers=headers)
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_export_company_4_results_quiz_2_json_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test6@test.com']}",
    }
    response = await ac.get('/company/4/quiz/2/results/export/json', headers=headers)
    assert response.status_code == 200


# ---------- Export company results for quiz specified csv ---------- #


@pytest.mark.asyncio
async def test_export_company_results_quiz_1_csv_not_auth(ac: AsyncClient, users_tokens):
    response = await ac.get('/company/4/quiz/1/results/export/csv')
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_export_company_results_quiz_1_csv_company_not_exists(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/company/40/quiz/1/results/export/csv', headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == 'Company does not exist'


@pytest.mark.asyncio
async def test_export_company_4_results_quiz_10_csv_quiz_not_exists(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/company/4/quiz/10/results/export/csv', headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == 'Quiz not found'


@pytest.mark.asyncio
async def test_export_company_4_results_quiz_1_csv_comp_4_not_allowed(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test4@test.com']}",
    }
    response = await ac.get('/company/4/quiz/1/results/export/csv', headers=headers)
    assert response.status_code == 403
    assert response.json().get('detail') == 'You are not allowed to export results'


@pytest.mark.asyncio
async def test_export_company_4_results_quiz_1_csv_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test6@test.com']}",
    }
    response = await ac.get('/company/4/quiz/1/results/export/csv', headers=headers)
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_export_company_4_results_quiz_2_csv_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test6@test.com']}",
    }
    response = await ac.get('/company/4/quiz/2/results/export/csv', headers=headers)
    assert response.status_code == 200
