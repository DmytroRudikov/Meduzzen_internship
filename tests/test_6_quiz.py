from httpx import AsyncClient
import pytest

# ---------- Create quiz ---------- #


@pytest.mark.asyncio
async def test_create_quiz_not_auth(ac: AsyncClient):
    payload = {
        "quiz_name": "quiz1",
        "description": "description",
        "questions": {1: "q1", 2: "q2"},
        "answer_options": [["a1", "a2", "a3", "a4"], ["a1", "a2", "a3", "a4"]],
        "correct_answer": ["a1", "a2"]
    }
    response = await ac.post('/company/1/quiz', json=payload)
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_create_quiz_company_not_found(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    payload = {
        "quiz_name": "quiz1",
        "description": "description",
        "questions": {1: "q1", 2: "q2"},
        "answer_options": [["a1", "a2", "a3", "a4"], ["a1", "a2", "a3", "a4"]],
        "correct_answer": ["a1", "a2"]
    }
    response = await ac.post('/company/100/quiz', json=payload, headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == "Company does not exist"


@pytest.mark.asyncio
async def test_create_quiz_not_owner_or_admin(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test4@test.com']}",
    }
    payload = {
        "quiz_name": "quiz1",
        "description": "description",
        "questions": {1: "q1", 2: "q2"},
        "answer_options": [["a1", "a2", "a3", "a4"], ["a1", "a2", "a3", "a4"]],
        "correct_answer": ["a1", "a2"]
    }
    response = await ac.post('/company/1/quiz', json=payload, headers=headers)
    assert response.status_code == 403
    assert response.json().get('detail') == "You are not allowed to create quizzes"


@pytest.mark.asyncio
async def test_create_quiz_one_comp_one_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    payload = {
        "quiz_name": "quiz1",
        "description": "description",
        "questions": {1: "q1", 2: "q2"},
        "answer_options": [["a1", "a2", "a3", "a4"], ["a1", "a2", "a3", "a4"]],
        "correct_answer": ["a1", "a2"]
    }
    response = await ac.post('/company/1/quiz', json=payload, headers=headers)
    assert response.status_code == 200
    assert response.json().get('detail') == 'success'


@pytest.mark.asyncio
async def test_create_quiz_one_comp_four_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test6@test.com']}",
    }
    payload = {
        "quiz_name": "quiz1",
        "description": "description",
        "questions": {1: "q1", 2: "q2"},
        "answer_options": [["a1", "a2", "a3", "a4"], ["a1", "a2", "a3", "a4"]],
        "correct_answer": ["a1", "a2"]
    }
    response = await ac.post('/company/4/quiz', json=payload, headers=headers)
    assert response.status_code == 200
    assert response.json().get('detail') == 'success'


@pytest.mark.asyncio
async def test_create_quiz_two_comp_four_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    payload = {
        "quiz_name": "quiz2",
        "description": "description",
        "questions": {1: "q1", 2: "q2"},
        "answer_options": [["a1", "a2", "a3", "a4"], ["a1", "a2", "a3", "a4"]],
        "correct_answer": ["a1", "a2"]
    }
    response = await ac.post('/company/4/quiz', json=payload, headers=headers)
    assert response.status_code == 200
    assert response.json().get('detail') == 'success'


# ---------- Get quiz ---------- #


@pytest.mark.asyncio
async def test_get_quizzes_comp_one_not_auth(ac: AsyncClient, users_tokens):
    response = await ac.get('/company/1/quizzes')
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_get_quizzes_comp_not_exists(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/company/100/quizzes', headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == 'Company does not exist'


@pytest.mark.asyncio
async def test_get_quizzes_comp_one_not_member(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/company/1/quizzes', headers=headers)
    assert response.status_code == 403
    assert response.json().get('detail') == 'You are not a member of the company'


@pytest.mark.asyncio
async def test_get_quizzes_comp_one_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test4@test.com']}",
    }
    response = await ac.get('/company/1/quizzes', headers=headers)
    assert response.status_code == 200
    assert len(response.json().get('items')) == 1


@pytest.mark.asyncio
async def test_get_quizzes_comp_four_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test4@test.com']}",
    }
    response = await ac.get('/company/4/quizzes', headers=headers)
    assert response.status_code == 200
    assert len(response.json().get('items')) == 2


@pytest.mark.asyncio
async def test_get_quiz_one_comp_one_not_auth(ac: AsyncClient, users_tokens):
    response = await ac.get('/company/1/quiz/1')
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_get_quiz_comp_not_exists(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.get('/company/100/quiz/1', headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == 'Company does not exist'


@pytest.mark.asyncio
async def test_get_quiz_one_comp_one_not_member(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/company/1/quiz/1', headers=headers)
    assert response.status_code == 403
    assert response.json().get('detail') == 'You are not a member of the company'


@pytest.mark.asyncio
async def test_get_quiz_not_exists(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.get('/company/1/quiz/100', headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == 'Quiz not found'


@pytest.mark.asyncio
async def test_get_quiz_one_comp_one_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.get('/company/1/quiz/1', headers=headers)
    assert response.status_code == 200
    assert response.json().get("quiz_record_id") == 1
    assert response.json().get("company_id") == 1
    assert response.json().get("quiz_id_in_company") == 1
    assert response.json().get("quiz_name") == "quiz1"
    assert response.json().get("description") == "description"


# ---------- Update quiz ---------- #

@pytest.mark.asyncio
async def test_update_quiz_not_auth(ac: AsyncClient):
    payload = {
        "quiz_name": "quiz1NEW",
        "description": "descriptionNEW",
    }
    response = await ac.put('/company/1/quiz/1', json=payload)
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_update_quiz_company_not_found(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    payload = {
        "quiz_name": "quiz1NEW",
        "description": "descriptionNEW",
    }
    response = await ac.put('/company/100/quiz/1', json=payload, headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == "Company does not exist"


@pytest.mark.asyncio
async def test_update_quiz_not_owner_or_admin(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test4@test.com']}",
    }
    payload = {
        "quiz_name": "quiz1NEW",
        "description": "descriptionNEW",
    }
    response = await ac.put('/company/1/quiz/1', json=payload, headers=headers)
    assert response.status_code == 403
    assert response.json().get('detail') == "You are not allowed to update quizzes"


@pytest.mark.asyncio
async def test_update_quiz_not_exists(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    payload = {
        "quiz_name": "quiz1NEW",
        "description": "descriptionNEW",
    }
    response = await ac.put('/company/1/quiz/100', headers=headers, json=payload)
    assert response.status_code == 404
    assert response.json().get('detail') == 'Quiz not found'


@pytest.mark.asyncio
async def test_update_quiz_one_comp_one_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    payload = {
        "quiz_name": "quiz1NEW",
        "description": "descriptionNEW",
    }
    response = await ac.put('/company/1/quiz/1', json=payload, headers=headers)
    assert response.status_code == 200
    assert response.json().get('detail') == "success"


@pytest.mark.asyncio
async def test_update_quiz_one_comp_four_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    payload = {
        "quiz_name": "quiz1NEW",
    }
    response = await ac.put('/company/4/quiz/1', json=payload, headers=headers)
    assert response.status_code == 200
    assert response.json().get('detail') == "success"


@pytest.mark.asyncio
async def test_get_quiz_one_comp_four_after_upd(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/company/4/quiz/1', headers=headers)
    assert response.status_code == 200
    assert response.json().get("quiz_record_id") == 2
    assert response.json().get("company_id") == 4
    assert response.json().get("quiz_id_in_company") == 1
    assert response.json().get("quiz_name") == "quiz1NEW"
    assert response.json().get("description") == "description"


@pytest.mark.asyncio
async def test_get_quiz_one_comp_one_after_upd(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.get('/company/1/quiz/1', headers=headers)
    assert response.status_code == 200
    assert response.json().get("quiz_record_id") == 1
    assert response.json().get("company_id") == 1
    assert response.json().get("quiz_id_in_company") == 1
    assert response.json().get("quiz_name") == "quiz1NEW"
    assert response.json().get("description") == "descriptionNEW"


# ---------- Delete quiz ---------- #


@pytest.mark.asyncio
async def test_delete_quiz_not_auth(ac: AsyncClient):
    response = await ac.delete('/company/1/quiz/1')
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_delete_quiz_company_not_found(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.delete('/company/100/quiz/1', headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == "Company does not exist"


@pytest.mark.asyncio
async def test_delete_quiz_not_owner_or_admin(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    response = await ac.delete('/company/1/quiz/1', headers=headers)
    assert response.status_code == 403
    assert response.json().get('detail') == "You are not allowed to delete quizzes"


@pytest.mark.asyncio
async def test_delete_quiz_not_exists(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.delete('/company/1/quiz/100', headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == 'Quiz not found'


@pytest.mark.asyncio
async def test_delete_quiz_one_comp_one_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.delete('/company/1/quiz/1', headers=headers)
    assert response.status_code == 200
    assert response.json().get('detail') == "success"


@pytest.mark.asyncio
async def test_get_quizzes_comp_one_after_delete(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.get('/company/1/quizzes', headers=headers)
    assert response.status_code == 200
    assert len(response.json().get('items')) == 0


# ---------- QUESTIONS ---------- #
# ---------- Get questions ---------- #


@pytest.mark.asyncio
async def test_get_questions_comp_four_not_auth(ac: AsyncClient, users_tokens):
    response = await ac.get('/company/4/quiz/1/questions')
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_get_questions_comp_not_exists(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/company/100/quiz/1/questions', headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == 'Company does not exist'


@pytest.mark.asyncio
async def test_get_questions_comp_four_not_member(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.get('/company/4/quiz/1/questions', headers=headers)
    assert response.status_code == 403
    assert response.json().get('detail') == 'You are not a member of the company'


@pytest.mark.asyncio
async def test_get_questions_quiz_not_exists(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/company/4/quiz/100/questions', headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == 'Quiz not found'


@pytest.mark.asyncio
async def test_get_questions_comp_four_quiz_one_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/company/4/quiz/1/questions', headers=headers)
    assert response.status_code == 200
    assert len(response.json().get('items')) == 2
    assert response.json().get('items')[0].get("correct_answer") is None
    assert response.json().get('items')[0].get("answer_options")[0] == "a1"
    assert response.json().get('items')[0].get("answer_options")[1] == "a2"
    assert response.json().get('items')[0].get("answer_options")[2] == "a3"
    assert response.json().get('items')[0].get("answer_options")[3] == "a4"
    assert response.json().get('items')[0].get("question") == "q1"
    assert response.json().get('items')[0].get("question_id_in_quiz") == 1
    assert response.json().get('items')[0].get("quiz_record_id") == 2


@pytest.mark.asyncio
async def test_get_questions_comp_four_quiz_two_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/company/4/quiz/2/questions', headers=headers)
    assert response.status_code == 200
    assert len(response.json().get('items')) == 2
    assert response.json().get('items')[1].get("correct_answer") is None
    assert response.json().get('items')[1].get("answer_options")[0] == "a1"
    assert response.json().get('items')[1].get("answer_options")[1] == "a2"
    assert response.json().get('items')[1].get("answer_options")[2] == "a3"
    assert response.json().get('items')[1].get("answer_options")[3] == "a4"
    assert response.json().get('items')[1].get("question") == "q2"
    assert response.json().get('items')[1].get("question_id_in_quiz") == 2
    assert response.json().get('items')[1].get("quiz_record_id") == 3


# ---------- Add new questions ---------- #


@pytest.mark.asyncio
async def test_add_questions_not_auth(ac: AsyncClient):
    payload = {
        "questions": {3: "q3", 4: "q4"},
        "answer_options": [["a1", "a2", "a3", "a4"], ["a1", "a2", "a3", "a4"]],
        "correct_answer": ["a3", "a4"]
    }
    response = await ac.post('/company/4/quiz/1/questions', json=payload)
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_add_questions_company_not_found(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    payload = {
        "questions": {3: "q3", 4: "q4"},
        "answer_options": [["a1", "a2", "a3", "a4"], ["a1", "a2", "a3", "a4"]],
        "correct_answer": ["a3", "a4"]
    }
    response = await ac.post('/company/100/quiz/1/questions', json=payload, headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == "Company does not exist"


@pytest.mark.asyncio
async def test_add_questions_not_owner_or_admin(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test4@test.com']}",
    }
    payload = {
        "questions": {3: "q3", 4: "q4"},
        "answer_options": [["a1", "a2", "a3", "a4"], ["a1", "a2", "a3", "a4"]],
        "correct_answer": ["a3", "a4"]
    }
    response = await ac.post('/company/4/quiz/1/questions', json=payload, headers=headers)
    assert response.status_code == 403
    assert response.json().get('detail') == "You are not allowed to add questions"
    

@pytest.mark.asyncio
async def test_add_questions_quiz_not_exists(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    payload = {
        "questions": {3: "q3", 4: "q4"},
        "answer_options": [["a1", "a2", "a3", "a4"], ["a1", "a2", "a3", "a4"]],
        "correct_answer": ["a3", "a4"]
    }
    response = await ac.post('/company/4/quiz/100/questions', headers=headers, json=payload)
    assert response.status_code == 404
    assert response.json().get('detail') == 'Quiz not found'


@pytest.mark.asyncio
async def test_add_new_questions_for_quiz_one_comp_four_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test6@test.com']}",
    }
    payload = {
        "questions": {3: "q3", 4: "q4"},
        "answer_options": [["a1", "a2", "a3", "a4"], ["a1", "a2", "a3", "a4"]],
        "correct_answer": ["a3", "a4"]
    }
    response = await ac.post('/company/4/quiz/1/questions', json=payload, headers=headers)
    assert response.status_code == 200
    assert response.json().get('detail') == 'success'
    

@pytest.mark.asyncio
async def test_get_questions_for_quiz_one_comp_four_after_add(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test6@test.com']}",
    }
    response = await ac.get('/company/4/quiz/1/questions', headers=headers)
    assert response.status_code == 200
    assert len(response.json().get('items')) == 4
    assert response.json().get('items')[3].get("correct_answer") is None
    assert response.json().get('items')[3].get("answer_options")[0] == "a1"
    assert response.json().get('items')[3].get("answer_options")[1] == "a2"
    assert response.json().get('items')[3].get("answer_options")[2] == "a3"
    assert response.json().get('items')[3].get("answer_options")[3] == "a4"
    assert response.json().get('items')[3].get("question") == "q4"
    assert response.json().get('items')[3].get("question_id_in_quiz") == 4
    assert response.json().get('items')[3].get("quiz_record_id") == 2


# ---------- Update questions ---------- #


@pytest.mark.asyncio
async def test_update_questions_not_auth(ac: AsyncClient):
    payload = {
        "questions": {1: "q1New"},
        "correct_answer": ["a2"]
    }
    response = await ac.put('/company/4/quiz/2/questions', json=payload)
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_update_questions_company_not_found(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    payload = {
        "questions": {1: "q1New"},
        "correct_answer": ["a2"]
    }
    response = await ac.put('/company/100/quiz/2/questions', json=payload, headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == "Company does not exist"


@pytest.mark.asyncio
async def test_update_questions_not_owner_or_admin(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    payload = {
        "questions": {1: "q1New"},
        "correct_answer": ["a2"]
    }
    response = await ac.put('/company/4/quiz/2/questions', json=payload, headers=headers)
    assert response.status_code == 403
    assert response.json().get('detail') == "You are not allowed to update questions"


@pytest.mark.asyncio
async def test_update_questions_quiz_not_exists(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    payload = {
        "questions": {1: "q1New"},
        "correct_answer": ["a2"]
    }
    response = await ac.put('/company/4/quiz/100/questions', headers=headers, json=payload)
    assert response.status_code == 404
    assert response.json().get('detail') == 'Quiz not found'


@pytest.mark.asyncio
async def test_update_questions_quiz_two_comp_four_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    payload = {
        "questions": {1: "q1New"},
        "correct_answer": ["a2"]
    }
    response = await ac.put('/company/4/quiz/2/questions', json=payload, headers=headers)
    assert response.status_code == 200
    assert response.json().get('detail') == "success"


@pytest.mark.asyncio
async def test_update_questions_quiz_one_comp_four_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test6@test.com']}",
    }
    payload = {
        "questions": {3: "q3", 4: "q4"},
        "answer_options": [["a5", "a6", "a7", "a8"], ["a5", "a6", "a7", "a8"]],
        "correct_answer": ["a5", "a6"]
    }
    response = await ac.put('/company/4/quiz/1/questions', json=payload, headers=headers)
    assert response.status_code == 200
    assert response.json().get('detail') == "success"


@pytest.mark.asyncio
async def test_get_questions_quiz_one_comp_four_after_upd(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/company/4/quiz/1/questions', headers=headers)
    assert response.status_code == 200
    assert len(response.json().get('items')) == 4
    assert response.json().get('items')[3].get("correct_answer") is None
    assert response.json().get('items')[3].get("answer_options")[0] == "a5"
    assert response.json().get('items')[3].get("answer_options")[1] == "a6"
    assert response.json().get('items')[3].get("answer_options")[2] == "a7"
    assert response.json().get('items')[3].get("answer_options")[3] == "a8"
    assert response.json().get('items')[3].get("question") == "q4"
    assert response.json().get('items')[3].get("question_id_in_quiz") == 4
    assert response.json().get('items')[3].get("quiz_record_id") == 2
    assert response.json().get('items')[2].get("answer_options")[0] == "a5"
    assert response.json().get('items')[2].get("answer_options")[1] == "a6"
    assert response.json().get('items')[2].get("answer_options")[2] == "a7"
    assert response.json().get('items')[2].get("answer_options")[3] == "a8"
    assert response.json().get('items')[2].get("question") == "q3"
    assert response.json().get('items')[2].get("question_id_in_quiz") == 3
    assert response.json().get('items')[2].get("quiz_record_id") == 2
    assert response.json().get('items')[1].get("answer_options")[0] == "a1"
    assert response.json().get('items')[1].get("answer_options")[1] == "a2"
    assert response.json().get('items')[1].get("answer_options")[2] == "a3"
    assert response.json().get('items')[1].get("answer_options")[3] == "a4"
    assert response.json().get('items')[1].get("question") == "q2"
    assert response.json().get('items')[1].get("question_id_in_quiz") == 2
    assert response.json().get('items')[1].get("quiz_record_id") == 2
    assert response.json().get('items')[0].get("answer_options")[0] == "a1"
    assert response.json().get('items')[0].get("answer_options")[1] == "a2"
    assert response.json().get('items')[0].get("answer_options")[2] == "a3"
    assert response.json().get('items')[0].get("answer_options")[3] == "a4"
    assert response.json().get('items')[0].get("question") == "q1"
    assert response.json().get('items')[0].get("question_id_in_quiz") == 1
    assert response.json().get('items')[0].get("quiz_record_id") == 2
    

@pytest.mark.asyncio
async def test_get_questions_quiz_two_comp_four_after_upd(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test4@test.com']}",
    }
    response = await ac.get('/company/4/quiz/2/questions', headers=headers)
    assert response.status_code == 200
    assert len(response.json().get('items')) == 2
    assert response.json().get('items')[1].get("correct_answer") is None
    assert response.json().get('items')[1].get("question") == "q1New"
    assert response.json().get('items')[1].get("question_id_in_quiz") == 1
    assert response.json().get('items')[1].get("quiz_record_id") == 3
    assert response.json().get('items')[1].get("answer_options")[0] == "a1"
    assert response.json().get('items')[1].get("answer_options")[1] == "a2"
    assert response.json().get('items')[1].get("answer_options")[2] == "a3"
    assert response.json().get('items')[1].get("answer_options")[3] == "a4"
    assert response.json().get('items')[0].get("question") == "q2"
    assert response.json().get('items')[0].get("question_id_in_quiz") == 2
    assert response.json().get('items')[0].get("quiz_record_id") == 3
    assert response.json().get('items')[0].get("answer_options")[0] == "a1"
    assert response.json().get('items')[0].get("answer_options")[1] == "a2"
    assert response.json().get('items')[0].get("answer_options")[2] == "a3"
    assert response.json().get('items')[0].get("answer_options")[3] == "a4"


# ---------- Delete questions ---------- #


@pytest.mark.asyncio
async def test_delete_questions_not_auth(ac: AsyncClient):
    payload = {
        "questions": [3, 4],
    }
    response = await ac.patch('/company/4/quiz/1/questions', json=payload)
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_delete_questions_company_not_found(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    payload = {
        "questions": [3, 4],
    }
    response = await ac.patch('/company/100/quiz/1/questions', headers=headers, json=payload)
    assert response.status_code == 404
    assert response.json().get('detail') == "Company does not exist"


@pytest.mark.asyncio
async def test_delete_questions_not_owner_or_admin(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    payload = {
        "questions": [3, 4],
    }
    response = await ac.patch('/company/4/quiz/1/questions', headers=headers, json=payload)
    assert response.status_code == 403
    assert response.json().get('detail') == "You are not allowed to delete questions"


@pytest.mark.asyncio
async def test_delete_questions_quiz_not_exists(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test6@test.com']}",
    }
    payload = {
        "questions": [3, 4],
    }
    response = await ac.patch('/company/4/quiz/100/questions', headers=headers, json=payload)
    assert response.status_code == 404
    assert response.json().get('detail') == 'Quiz not found'


@pytest.mark.asyncio
async def test_delete_questions_quiz_one_not_enough_questions_left(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test6@test.com']}",
    }
    payload = {
        "questions": [1, 3, 4],
    }
    response = await ac.patch('/company/4/quiz/1/questions', headers=headers, json=payload)
    assert response.status_code == 403
    assert response.json().get('detail') == 'Quiz must include at least 2 questions'


@pytest.mark.asyncio
async def test_delete_questions_quiz_one_comp_four_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    payload = {
        "questions": [3, 4],
    }
    response = await ac.patch('/company/4/quiz/1/questions', headers=headers, json=payload)
    assert response.status_code == 200
    assert response.json().get('detail') == "success"


@pytest.mark.asyncio
async def test_get_questions_quiz_one_comp_four_after_delete(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test4@test.com']}",
    }
    response = await ac.get('/company/4/quiz/1/questions', headers=headers)
    assert response.status_code == 200
    assert len(response.json().get('items')) == 2
    assert response.json().get('items')[1].get("correct_answer") is None
    assert response.json().get('items')[1].get("answer_options")[0] == "a1"
    assert response.json().get('items')[1].get("answer_options")[1] == "a2"
    assert response.json().get('items')[1].get("answer_options")[2] == "a3"
    assert response.json().get('items')[1].get("answer_options")[3] == "a4"
    assert response.json().get('items')[1].get("question") == "q2"
    assert response.json().get('items')[1].get("question_id_in_quiz") == 2
    assert response.json().get('items')[1].get("quiz_record_id") == 2
