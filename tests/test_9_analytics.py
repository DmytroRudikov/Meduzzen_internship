from httpx import AsyncClient
import pytest

# ---------- Get my avg result ---------- #


@pytest.mark.asyncio
async def test_get_my_avg_result_not_auth(ac: AsyncClient, users_tokens):
    response = await ac.get('/my_average_result')
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_get_my_avg_result_user_4_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test4@test.com']}",
    }
    response = await ac.get('/my_average_result', headers=headers)
    assert response.status_code == 200
    assert response.json() == 1.5


@pytest.mark.asyncio
async def test_get_my_avg_result_user_6_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test6@test.com']}",
    }
    response = await ac.get('/my_average_result', headers=headers)
    assert response.status_code == 200
    assert response.json() == 2


# ---------- Get my avg list of results ---------- #


@pytest.mark.asyncio
async def test_get_my_avg_results_not_auth(ac: AsyncClient, users_tokens):
    response = await ac.get('/my_average_results')
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_get_my_avg_results_user_4_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test4@test.com']}",
    }
    response = await ac.get('/my_average_results', headers=headers)
    assert response.status_code == 200
    assert len(response.json()) == 5
    assert response.json()[0].get("company_id") == 4
    assert response.json()[0].get("quiz_id_in_company") == 1
    assert response.json()[0].get("average_result") == 1
    assert response.json()[1].get("company_id") == 4
    assert response.json()[1].get("quiz_id_in_company") == 2
    assert response.json()[1].get("average_result") == 2
    assert response.json()[2].get("company_id") == 4
    assert response.json()[2].get("quiz_id_in_company") == 2
    assert response.json()[2].get("average_result") == 1.5
    assert response.json()[3].get("company_id") == 4
    assert response.json()[3].get("quiz_id_in_company") == 2
    assert response.json()[3].get("average_result") == 1.7
    assert response.json()[4].get("company_id") == 4
    assert response.json()[4].get("quiz_id_in_company") == 2
    assert response.json()[4].get("average_result") == 1.3


@pytest.mark.asyncio
async def test_get_my_avg_results_user_6_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test6@test.com']}",
    }
    response = await ac.get('/my_average_results', headers=headers)
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0].get("company_id") == 4
    assert response.json()[0].get("quiz_id_in_company") == 2
    assert response.json()[0].get("average_result") == 2
    assert response.json()[1].get("company_id") == 4
    assert response.json()[1].get("quiz_id_in_company") == 2
    assert response.json()[1].get("average_result") == 2


# ---------- Get my quizzes passed ---------- #


@pytest.mark.asyncio
async def test_get_my_quizzes_passed_not_auth(ac: AsyncClient, users_tokens):
    response = await ac.get('/my_quizzes_passed')
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_get_my_quizzes_passed_user_4_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test4@test.com']}",
    }
    response = await ac.get('/my_quizzes_passed', headers=headers)
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0].get("company_id") == 4
    assert response.json()[0].get("quiz_id_in_company") == 1
    assert response.json()[1].get("company_id") == 4
    assert response.json()[1].get("quiz_id_in_company") == 2


@pytest.mark.asyncio
async def test_get_my_quizzes_passed_user_6_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test6@test.com']}",
    }
    response = await ac.get('/my_quizzes_passed', headers=headers)
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0].get("company_id") == 4
    assert response.json()[0].get("quiz_id_in_company") == 2


# ---------- Get all company members results ---------- #


@pytest.mark.asyncio
async def test_get_all_comp_members_results_comp_4_not_auth(ac: AsyncClient, users_tokens):
    response = await ac.get('/company/4/members/results')
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_get_all_comp_members_results_comp_not_exists(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/company/40/members/results', headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == 'Company does not exist'


@pytest.mark.asyncio
async def test_get_all_comp_members_results_comp_4_not_allowed(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test4@test.com']}",
    }
    response = await ac.get('/company/4/members/results', headers=headers)
    assert response.status_code == 403
    assert response.json().get('detail') == 'You are not allowed to see results'


@pytest.mark.asyncio
async def test_get_all_comp_members_results_comp_4_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/company/4/members/results', headers=headers)
    assert response.status_code == 200
    assert len(response.json()) == 7
    assert response.json()[0].get("user_id") == 4
    assert response.json()[0].get("quiz_id_in_company") == 1
    assert response.json()[0].get("average_result") == 1
    assert response.json()[1].get("user_id") == 4
    assert response.json()[1].get("quiz_id_in_company") == 2
    assert response.json()[1].get("average_result") == 2
    assert response.json()[2].get("user_id") == 6
    assert response.json()[2].get("quiz_id_in_company") == 2
    assert response.json()[2].get("average_result") == 2
    assert response.json()[3].get("user_id") == 4
    assert response.json()[3].get("quiz_id_in_company") == 2
    assert response.json()[3].get("average_result") == 1.5
    assert response.json()[4].get("user_id") == 6
    assert response.json()[4].get("quiz_id_in_company") == 2
    assert response.json()[4].get("average_result") == 2
    assert response.json()[5].get("user_id") == 4
    assert response.json()[5].get("quiz_id_in_company") == 2
    assert response.json()[5].get("average_result") == 1.7
    assert response.json()[6].get("user_id") == 4
    assert response.json()[6].get("quiz_id_in_company") == 2
    assert response.json()[6].get("average_result") == 1.3




@pytest.mark.asyncio
async def test_get_all_comp_members_results_comp_1_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.get('/company/1/members/results', headers=headers)
    assert response.status_code == 200
    assert len(response.json()) == 0


# ---------- Get results for company member ---------- #


@pytest.mark.asyncio
async def test_get_all_results_comp_4_mem_2_not_auth(ac: AsyncClient, users_tokens):
    response = await ac.get('/company/4/member/2/results')
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_get_all_results_comp_4_mem_2_comp_not_exists(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test6@test.com']}",
    }
    response = await ac.get('/company/40/member/2/results', headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == 'Company does not exist'


@pytest.mark.asyncio
async def test_get_all_results_comp_4_mem_3_not_allowed(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test4@test.com']}",
    }
    response = await ac.get('/company/4/member/2/results', headers=headers)
    assert response.status_code == 403
    assert response.json().get('detail') == 'You are not allowed to see results'


@pytest.mark.asyncio
async def test_get_all_results_comp_4_mem_20_mem_not_exists(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/company/4/member/20/results', headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == 'Company member with id 20 not found'


@pytest.mark.asyncio
async def test_get_all_results_comp_4_mem_2_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test6@test.com']}",
    }
    response = await ac.get('/company/4/member/2/results', headers=headers)
    assert response.status_code == 200
    assert len(response.json()) == 5
    assert response.json()[0].get("user_id") == 4
    assert response.json()[0].get("quiz_id_in_company") == 1
    assert response.json()[0].get("average_result") == 1
    assert response.json()[1].get("user_id") == 4
    assert response.json()[1].get("quiz_id_in_company") == 2
    assert response.json()[1].get("average_result") == 2
    assert response.json()[2].get("user_id") == 4
    assert response.json()[2].get("quiz_id_in_company") == 2
    assert response.json()[2].get("average_result") == 1.5
    assert response.json()[3].get("user_id") == 4
    assert response.json()[3].get("quiz_id_in_company") == 2
    assert response.json()[3].get("average_result") == 1.7
    assert response.json()[4].get("user_id") == 4
    assert response.json()[4].get("quiz_id_in_company") == 2
    assert response.json()[4].get("average_result") == 1.3


@pytest.mark.asyncio
async def test_get_all_results_comp_4_mem_3_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/company/4/member/3/results', headers=headers)
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0].get("user_id") == 6
    assert response.json()[0].get("quiz_id_in_company") == 2
    assert response.json()[0].get("average_result") == 2
    assert response.json()[1].get("user_id") == 6
    assert response.json()[1].get("quiz_id_in_company") == 2
    assert response.json()[1].get("average_result") == 2


@pytest.mark.asyncio
async def test_get_all_results_comp_1_mem_1_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.get('/company/1/member/1/results', headers=headers)
    assert response.status_code == 200
    assert len(response.json()) == 0


# ---------- Get members passed ---------- #


@pytest.mark.asyncio
async def test_get_members_passed_not_auth(ac: AsyncClient, users_tokens):
    response = await ac.get('/company/4/members_passed')
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_get_members_passed_comp_not_exists(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/company/40/members_passed', headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == 'Company does not exist'


@pytest.mark.asyncio
async def test_get_members_passed_comp_4_not_allowed(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test4@test.com']}",
    }
    response = await ac.get('/company/4/members_passed', headers=headers)
    assert response.status_code == 403
    assert response.json().get('detail') == 'You are not allowed to see results'


@pytest.mark.asyncio
async def test_get_members_passed_comp_4_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/company/4/members_passed', headers=headers)
    assert response.status_code == 200
    assert len(response.json()) == 3
    assert response.json()[0].get("company_member_id") == 2
    assert response.json()[0].get("quiz_id_in_company") == 1
    assert response.json()[1].get("company_member_id") == 2
    assert response.json()[1].get("quiz_id_in_company") == 2
    assert response.json()[2].get("company_member_id") == 3
    assert response.json()[2].get("quiz_id_in_company") == 2


@pytest.mark.asyncio
async def test_get_members_passed_comp_1_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.get('/company/1/members_passed', headers=headers)
    assert response.status_code == 200
    assert len(response.json()) == 0
