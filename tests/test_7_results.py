from httpx import AsyncClient
import pytest

# ---------- Send answers ---------- #


@pytest.mark.asyncio
async def test_send_answers_not_auth(ac: AsyncClient):
    payload = {
        "answers": {1: "a1", 2: "a3"},
    }
    response = await ac.post('/company/4/quiz/1/send_answers', json=payload)
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_send_answers_company_not_found(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    payload = {
        "answers": {1: "a1", 2: "a3"},
    }
    response = await ac.post('/company/40/quiz/1/send_answers', json=payload, headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == "Company does not exist"


@pytest.mark.asyncio
async def test_send_answers_not_member(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    payload = {
        "answers": {1: "a1", 2: "a3"},
    }
    response = await ac.post('/company/4/quiz/1/send_answers', json=payload, headers=headers)
    assert response.status_code == 403
    assert response.json().get('detail') == "You are not a member to take the quiz"


@pytest.mark.asyncio
async def test_send_answers_quiz_not_exists(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test4@test.com']}",
    }
    payload = {
        "answers": {1: "a1", 2: "a3"},
    }
    response = await ac.post('/company/4/quiz/3/send_answers', json=payload, headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == "Quiz not found"


@pytest.mark.asyncio
async def test_send_answers_not_all_questions_answered(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test4@test.com']}",
    }
    payload = {
        "answers": {1: "a1"},
    }
    response = await ac.post('/company/4/quiz/1/send_answers', json=payload, headers=headers)
    assert response.status_code == 403
    assert response.json().get('detail') == "Not all questions were answered"


@pytest.mark.asyncio
async def test_send_answers_empty_question(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test4@test.com']}",
    }
    payload = {
        "answers": {1: "a1", 2: ""},
    }
    response = await ac.post('/company/4/quiz/1/send_answers', json=payload, headers=headers)
    assert response.status_code == 403
    assert response.json().get('detail') == "Not all questions were answered"


@pytest.mark.asyncio
async def test_send_answers_none_question(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test4@test.com']}",
    }
    payload = {
        "answers": {1: "a1", 2: None},
    }
    response = await ac.post('/company/4/quiz/1/send_answers', json=payload, headers=headers)
    assert response.status_code == 403
    assert response.json().get('detail') == "Not all questions were answered"


@pytest.mark.asyncio
async def test_send_answers_type_error(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test4@test.com']}",
    }
    payload = {
        "answers": "1: a1, 2: a2",
    }
    response = await ac.post('/company/4/quiz/1/send_answers', json=payload, headers=headers)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_send_answers_company_four_quiz_one_user_four_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test4@test.com']}",
    }
    payload = {
        "answers": {1: "a1", 2: "a3"},
    }
    response = await ac.post('/company/4/quiz/1/send_answers', json=payload, headers=headers)
    assert response.status_code == 200
    assert response.json().get('detail') == "success"


@pytest.mark.asyncio
async def test_send_answers_company_four_quiz_two_user_four_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test4@test.com']}",
    }
    payload = {
        "answers": {1: "a2", 2: "a2"},
    }
    response = await ac.post('/company/4/quiz/2/send_answers', json=payload, headers=headers)
    assert response.status_code == 200
    assert response.json().get('detail') == "success"


@pytest.mark.asyncio
async def test_send_answers_company_four_quiz_two_user_six_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test6@test.com']}",
    }
    payload = {
        "answers": {1: "a2", 2: "a2"},
    }
    response = await ac.post('/company/4/quiz/2/send_answers', json=payload, headers=headers)
    assert response.status_code == 200
    assert response.json().get('detail') == "success"


# ---------- Get results for user ---------- #


@pytest.mark.asyncio
async def test_get_results_user_four_not_auth(ac: AsyncClient, users_tokens):
    response = await ac.get('/quizzes/my_results')
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_get_results_user_four_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test4@test.com']}",
    }
    response = await ac.get('/quizzes/my_results', headers=headers)
    assert response.status_code == 200
    assert len(response.json().get('items')) == 2
    assert response.json().get('items')[0].get("user_id") == 4
    assert response.json().get('items')[0].get("company_id") == 4
    assert response.json().get('items')[0].get("average_result") == 1
    assert response.json().get('items')[0].get("number_of_questions") == 2
    assert response.json().get('items')[0].get("correct_answers") == 1
    assert response.json().get('items')[1].get("user_id") == 4
    assert response.json().get('items')[1].get("company_id") == 4
    assert response.json().get('items')[1].get("average_result") == 2
    assert response.json().get('items')[1].get("number_of_questions") == 2
    assert response.json().get('items')[1].get("correct_answers") == 2


@pytest.mark.asyncio
async def test_get_results_user_six_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test6@test.com']}",
    }
    response = await ac.get('/quizzes/my_results', headers=headers)
    assert response.status_code == 200
    assert len(response.json().get('items')) == 1
    assert response.json().get('items')[0].get("user_id") == 6
    assert response.json().get('items')[0].get("company_id") == 4
    assert response.json().get('items')[0].get("average_result") == 2
    assert response.json().get('items')[0].get("number_of_questions") == 2
    assert response.json().get('items')[0].get("correct_answers") == 2


@pytest.mark.asyncio
async def test_get_results_user_one_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.get('/quizzes/my_results', headers=headers)
    assert response.status_code == 200
    assert len(response.json().get('items')) == 0


# ---------- Get results for company member ---------- #


@pytest.mark.asyncio
async def test_get_results_comp_mem_not_auth(ac: AsyncClient, users_tokens):
    response = await ac.get('/company/4/member/2/quizzes/results')
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_get_results_comp_mem_comp_not_exists(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test4@test.com']}",
    }
    response = await ac.get('/company/40/member/2/quizzes/results', headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == 'Company does not exist'


@pytest.mark.asyncio
async def test_get_results_comp_mem_mem_not_exists(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test4@test.com']}",
    }
    response = await ac.get('/company/4/member/20/quizzes/results', headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == 'Company member with id 20 not found'


@pytest.mark.asyncio
async def test_get_results_comp_mem_not_allowed(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.get('/company/4/member/2/quizzes/results', headers=headers)
    assert response.status_code == 403
    assert response.json().get('detail') == 'You are not allowed to see results'


@pytest.mark.asyncio
async def test_get_results_comp_mem_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test6@test.com']}",
    }
    response = await ac.get('/company/4/member/2/quizzes/results', headers=headers)
    assert response.status_code == 200
    assert len(response.json().get('items')) == 2
    assert response.json().get('items')[0].get("user_id") == 4
    assert response.json().get('items')[0].get("company_id") == 4
    assert response.json().get('items')[0].get("average_result") == 1
    assert response.json().get('items')[0].get("number_of_questions") == 2
    assert response.json().get('items')[0].get("correct_answers") == 1
    assert response.json().get('items')[1].get("user_id") == 4
    assert response.json().get('items')[1].get("company_id") == 4
    assert response.json().get('items')[1].get("average_result") == 2
    assert response.json().get('items')[1].get("number_of_questions") == 2
    assert response.json().get('items')[1].get("correct_answers") == 2


# ---------- Get updated results for company member by quiz ---------- #


@pytest.mark.asyncio
async def test_send_answers_company_four_quiz_two_user_four_v_2_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test4@test.com']}",
    }
    payload = {
        "answers": {1: "a4", 2: "a2"},
    }
    response = await ac.post('/company/4/quiz/2/send_answers', json=payload, headers=headers)
    assert response.status_code == 200
    assert response.json().get('detail') == "success"


@pytest.mark.asyncio
async def test_send_answers_company_four_quiz_two_user_six_v_2_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test6@test.com']}",
    }
    payload = {
        "answers": {1: "a2", 2: "a2"},
    }
    response = await ac.post('/company/4/quiz/2/send_answers', json=payload, headers=headers)
    assert response.status_code == 200
    assert response.json().get('detail') == "success"


@pytest.mark.asyncio
async def test_get_results_comp_mem_after_upd_not_auth(ac: AsyncClient, users_tokens):
    response = await ac.get('/company/4/member/2/quiz/2/results')
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_get_results_comp_mem_after_upd_comp_not_exists(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test4@test.com']}",
    }
    response = await ac.get('/company/40/member/2/quiz/2/results', headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == 'Company does not exist'


@pytest.mark.asyncio
async def test_get_results_comp_mem_after_upd_mem_not_exists(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test4@test.com']}",
    }
    response = await ac.get('/company/4/member/20/quiz/2/results', headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == 'Company member with id 20 not found'


@pytest.mark.asyncio
async def test_get_results_comp_mem_after_upd_not_allowed(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test4@test.com']}",
    }
    response = await ac.get('/company/4/member/3/quiz/2/results', headers=headers)
    assert response.status_code == 403
    assert response.json().get('detail') == 'You are not allowed to see results'


@pytest.mark.asyncio
async def test_get_results_comp_mem_after_upd_quiz_not_found(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test6@test.com']}",
    }
    response = await ac.get('/company/4/member/3/quiz/7/results', headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == 'Quiz not found'


@pytest.mark.asyncio
async def test_get_results_comp_mem_2_for_quiz_2_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test4@test.com']}",
    }
    response = await ac.get('/company/4/member/2/quiz/2/results', headers=headers)
    assert response.status_code == 200
    assert len(response.json().get('items')) == 2
    assert response.json().get('items')[0].get("user_id") == 4
    assert response.json().get('items')[0].get("company_id") == 4
    assert response.json().get('items')[0].get("average_result") == 2
    assert response.json().get('items')[0].get("number_of_questions") == 2
    assert response.json().get('items')[0].get("correct_answers") == 2
    assert response.json().get('items')[1].get("user_id") == 4
    assert response.json().get('items')[1].get("company_id") == 4
    assert response.json().get('items')[1].get("average_result") == 1.5
    assert response.json().get('items')[1].get("number_of_questions") == 4
    assert response.json().get('items')[1].get("correct_answers") == 3


@pytest.mark.asyncio
async def test_get_results_comp_mem_3_for_quiz_2_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/company/4/member/3/quiz/2/results', headers=headers)
    assert response.status_code == 200
    assert len(response.json().get('items')) == 2
    assert response.json().get('items')[0].get("user_id") == 6
    assert response.json().get('items')[0].get("company_id") == 4
    assert response.json().get('items')[0].get("average_result") == 2
    assert response.json().get('items')[0].get("number_of_questions") == 2
    assert response.json().get('items')[0].get("correct_answers") == 2
    assert response.json().get('items')[1].get("user_id") == 6
    assert response.json().get('items')[1].get("company_id") == 4
    assert response.json().get('items')[1].get("average_result") == 2
    assert response.json().get('items')[1].get("number_of_questions") == 4
    assert response.json().get('items')[1].get("correct_answers") == 4


# ---------- Get all results for company ---------- #


@pytest.mark.asyncio
async def test_get_all_results_comp_4_not_auth(ac: AsyncClient, users_tokens):
    response = await ac.get('/company/4/quizzes/results')
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_get_all_results_for_comp_comp_not_exists(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test4@test.com']}",
    }
    response = await ac.get('/company/40/quizzes/results', headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == 'Company does not exist'


@pytest.mark.asyncio
async def test_get_all_results_comp_4_not_allowed(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test4@test.com']}",
    }
    response = await ac.get('/company/4/quizzes/results', headers=headers)
    assert response.status_code == 403
    assert response.json().get('detail') == 'You are not allowed to see results'


@pytest.mark.asyncio
async def test_get_all_results_comp_4_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/company/4/quizzes/results', headers=headers)
    assert response.status_code == 200
    assert len(response.json().get('items')) == 5


@pytest.mark.asyncio
async def test_get_all_results_comp_1_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.get('/company/1/quizzes/results', headers=headers)
    assert response.status_code == 200
    assert len(response.json().get('items')) == 0


# ---------- Get all results for company by quiz ---------- #


@pytest.mark.asyncio
async def test_get_all_results_comp_4_quiz_2_not_auth(ac: AsyncClient, users_tokens):
    response = await ac.get('/company/4/quiz/2/results')
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_get_all_results_for_comp_4_quiz_2_comp_not_exists(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test4@test.com']}",
    }
    response = await ac.get('/company/40/quiz/2/results', headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == 'Company does not exist'


@pytest.mark.asyncio
async def test_get_all_results_comp_4_quiz_2_not_allowed(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test4@test.com']}",
    }
    response = await ac.get('/company/4/quiz/2/results', headers=headers)
    assert response.status_code == 403
    assert response.json().get('detail') == 'You are not allowed to see results'


@pytest.mark.asyncio
async def test_get_all_results_comp_4_quiz_2_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/company/4/quiz/2/results', headers=headers)
    assert response.status_code == 200
    assert len(response.json().get('items')) == 4


@pytest.mark.asyncio
async def test_get_all_results_comp_4_quiz_1_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/company/4/quiz/1/results', headers=headers)
    assert response.status_code == 200
    assert len(response.json().get('items')) == 1


# ---------- Get average result for company member ---------- #


@pytest.mark.asyncio
async def test_get_average_result_comp_4_mem_2_not_auth(ac: AsyncClient, users_tokens):
    response = await ac.get('/company/4/member/2/average_result')
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_get_average_result_comp_4_mem_2_comp_not_exists(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test4@test.com']}",
    }
    response = await ac.get('/company/40/member/2/average_result', headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == 'Company does not exist'


@pytest.mark.asyncio
async def test_get_average_result_comp_4_mem_3_not_allowed(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test4@test.com']}",
    }
    response = await ac.get('/company/4/member/3/average_result', headers=headers)
    assert response.status_code == 403
    assert response.json().get('detail') == 'You are not allowed to see results'


@pytest.mark.asyncio
async def test_get_average_result_comp_4_mem_2_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/company/4/member/2/average_result', headers=headers)
    assert response.status_code == 200
    assert response.json() == 1.5


@pytest.mark.asyncio
async def test_send_answers_company_four_quiz_two_user_four_v_3_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test4@test.com']}",
    }
    payload = {
        "answers": {1: "a2", 2: "a2"},
    }
    response = await ac.post('/company/4/quiz/2/send_answers', json=payload, headers=headers)
    assert response.status_code == 200
    assert response.json().get('detail') == "success"


@pytest.mark.asyncio
async def test_send_answers_company_four_quiz_two_user_four_v_4_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test4@test.com']}",
    }
    payload = {
        "answers": {1: "a4", 2: "a4"},
    }
    response = await ac.post('/company/4/quiz/2/send_answers', json=payload, headers=headers)
    assert response.status_code == 200
    assert response.json().get('detail') == "success"


@pytest.mark.asyncio
async def test_get_results_comp_mem_2_for_quiz_2_latest_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test4@test.com']}",
    }
    response = await ac.get('/company/4/member/2/quiz/2/results', headers=headers)
    assert response.status_code == 200
    assert len(response.json().get('items')) == 4
    assert response.json().get('items')[0].get("user_id") == 4
    assert response.json().get('items')[0].get("company_id") == 4
    assert response.json().get('items')[0].get("average_result") == 2
    assert response.json().get('items')[0].get("number_of_questions") == 2
    assert response.json().get('items')[0].get("correct_answers") == 2
    assert response.json().get('items')[1].get("user_id") == 4
    assert response.json().get('items')[1].get("company_id") == 4
    assert response.json().get('items')[1].get("average_result") == 1.5
    assert response.json().get('items')[1].get("number_of_questions") == 4
    assert response.json().get('items')[1].get("correct_answers") == 3
    assert response.json().get('items')[2].get("user_id") == 4
    assert response.json().get('items')[2].get("company_id") == 4
    assert response.json().get('items')[2].get("average_result") == 1.7
    assert response.json().get('items')[2].get("number_of_questions") == 6
    assert response.json().get('items')[2].get("correct_answers") == 5
    assert response.json().get('items')[3].get("user_id") == 4
    assert response.json().get('items')[3].get("company_id") == 4
    assert response.json().get('items')[3].get("average_result") == 1.3
    assert response.json().get('items')[3].get("number_of_questions") == 8
    assert response.json().get('items')[3].get("correct_answers") == 5


@pytest.mark.asyncio
async def test_get_average_result_comp_4_mem_2_after_upd_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/company/4/member/2/average_result', headers=headers)
    assert response.status_code == 200
    assert response.json() == 1.5


# ---------- Get average result for user in the system ---------- #


@pytest.mark.asyncio
async def test_get_average_result_user_4_not_auth(ac: AsyncClient, users_tokens):
    response = await ac.get('/user/4/average_result')
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_get_average_result_user_not_found(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test4@test.com']}",
    }
    response = await ac.get('/user/20/average_result', headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == 'User with this id does not exist'


@pytest.mark.asyncio
async def test_get_average_result_user_4_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/user/4/average_result', headers=headers)
    assert response.status_code == 200
    assert response.json() == 1.5


@pytest.mark.asyncio
async def test_get_average_result_user_6_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.get('/user/6/average_result', headers=headers)
    assert response.status_code == 200
    assert response.json() == 2
