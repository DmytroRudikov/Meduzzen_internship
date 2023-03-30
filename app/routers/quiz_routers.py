import sys
import os
sys.path.append(os.getcwd())

from databases import Database
from app.schemas import member_schemas, user_schemas, quiz_schemas
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination import Page, paginate
from app.services.crud_company import CompanyCrud
from app.services.crud_member import MemberCrud
from app.services.crud_quiz import QuizCrud
from app.core.db_config import get_sql_db
from app.core.authorisation import get_current_user
from typing import List

router = APIRouter()


@router.get("/company/{company_id}/quizzes", response_model=Page[quiz_schemas.Quiz])
async def get_company_quizzes(company_id: int, db: Database = Depends(get_sql_db), user: user_schemas.User = Depends(get_current_user)) -> Page[quiz_schemas.Quiz]:
    crud_company = CompanyCrud(db=db)
    await crud_company.company_exists(company_id=company_id)
    crud_member = MemberCrud(db=db)
    member = await crud_member.get_member(company_id=company_id, user_id=user.id)
    if not member:
        raise HTTPException(status_code=403, detail="You are not a member of the company")
    crud_quiz = QuizCrud(db=db)
    quizzes = await crud_quiz.get_all_quizzes(company_id=company_id)
    return paginate(quizzes)


@router.get("/company/{company_id}/quiz/{quiz_id}", response_model=quiz_schemas.Quiz)
async def get_company_quiz(company_id: int, quiz_id: int, db: Database = Depends(get_sql_db), user: user_schemas.User = Depends(get_current_user)) -> quiz_schemas.Quiz:
    crud_company = CompanyCrud(db=db)
    await crud_company.company_exists(company_id=company_id)
    crud_member = MemberCrud(db=db)
    member = await crud_member.get_member(company_id=company_id, user_id=user.id)
    if not member:
        raise HTTPException(status_code=403, detail="You are not a member of the company")
    crud_quiz = QuizCrud(db=db)
    quiz = await crud_quiz.get_quiz(company_id=company_id, quiz_id_in_company=quiz_id)
    return quiz


@router.get("/company/{company_id}/quiz/{quiz_id}/questions", response_model=Page[quiz_schemas.Questions])
async def get_quiz_questions(company_id: int, quiz_id: int, db: Database = Depends(get_sql_db), user: user_schemas.User = Depends(get_current_user)) -> Page[quiz_schemas.Questions]:
    crud_company = CompanyCrud(db=db)
    await crud_company.company_exists(company_id=company_id)
    crud_member = MemberCrud(db=db)
    member = await crud_member.get_member(company_id=company_id, user_id=user.id)
    if not member:
        raise HTTPException(status_code=403, detail="You are not a member of the company")
    crud_quiz = QuizCrud(db=db)
    questions = await crud_quiz.get_all_questions_for_the_quiz(company_id=company_id, quiz_id_in_company=quiz_id)
    return paginate(questions)


@router.post("/company/{company_id}/quiz", status_code=200)
async def create_quiz(company_id: int, create_quiz_form: quiz_schemas.CreateQuiz, db: Database = Depends(get_sql_db), user: user_schemas.User = Depends(get_current_user)):
    crud_company = CompanyCrud(db=db)
    await crud_company.company_exists(company_id=company_id)
    crud_member = MemberCrud(db=db)
    member = await crud_member.get_member(company_id=company_id, user_id=user.id)
    if not member or member.role not in ["owner", "admin"]:
        raise HTTPException(status_code=403, detail="You are not allowed to create quizzes")
    crud_quiz = QuizCrud(db=db)
    return await crud_quiz.create_quiz_with_questions(company_id=company_id, create_quiz_form=create_quiz_form)


@router.post("/company/{company_id}/quiz/{quiz_id}/questions", status_code=200)
async def add_questions(company_id: int, quiz_id: int, new_questions: quiz_schemas.UpdateQuestions, db: Database = Depends(get_sql_db), user: user_schemas.User = Depends(get_current_user)):
    crud_company = CompanyCrud(db=db)
    await crud_company.company_exists(company_id=company_id)
    crud_member = MemberCrud(db=db)
    member = await crud_member.get_member(company_id=company_id, user_id=user.id)
    if not member or member.role not in ["owner", "admin"]:
        raise HTTPException(status_code=403, detail="You are not allowed to add questions")
    crud_quiz = QuizCrud(db=db)
    return await crud_quiz.add_questions(company_id=company_id, quiz_id_in_company=quiz_id, new_questions=new_questions)


@router.put("/company/{company_id}/quiz/{quiz_id}", status_code=200)
async def update_quiz(company_id: int, quiz_id: int, update_quiz_form: quiz_schemas.UpdateQuiz, db: Database = Depends(get_sql_db), user: user_schemas.User = Depends(get_current_user)):
    crud_company = CompanyCrud(db=db)
    await crud_company.company_exists(company_id=company_id)
    crud_member = MemberCrud(db=db)
    member = await crud_member.get_member(company_id=company_id, user_id=user.id)
    if not member or member.role not in ["owner", "admin"]:
        raise HTTPException(status_code=403, detail="You are not allowed to update quizzes")
    crud_quiz = QuizCrud(db=db)
    return await crud_quiz.update_quiz(company_id=company_id, quiz_id_in_company=quiz_id, update_quiz_form=update_quiz_form)


@router.put("/company/{company_id}/quiz/{quiz_id}/questions", status_code=200)
async def update_questions(company_id: int, quiz_id: int, update_questions_form: quiz_schemas.UpdateQuestions, db: Database = Depends(get_sql_db), user: user_schemas.User = Depends(get_current_user)):
    crud_company = CompanyCrud(db=db)
    await crud_company.company_exists(company_id=company_id)
    crud_member = MemberCrud(db=db)
    member = await crud_member.get_member(company_id=company_id, user_id=user.id)
    if not member or member.role not in ["owner", "admin"]:
        raise HTTPException(status_code=403, detail="You are not allowed to update questions")
    crud_quiz = QuizCrud(db=db)
    return await crud_quiz.update_questions(company_id=company_id, quiz_id_in_company=quiz_id, update_questions_form=update_questions_form)


@router.delete("/company/{company_id}/quiz/{quiz_id}", status_code=200)
async def delete_quiz(company_id: int, quiz_id: int, db: Database = Depends(get_sql_db), user: user_schemas.User = Depends(get_current_user)):
    crud_company = CompanyCrud(db=db)
    await crud_company.company_exists(company_id=company_id)
    crud_member = MemberCrud(db=db)
    member = await crud_member.get_member(company_id=company_id, user_id=user.id)
    if not member or member.role not in ["owner", "admin"]:
        raise HTTPException(status_code=403, detail="You are not allowed to delete quizzes")
    crud_quiz = QuizCrud(db=db)
    return await crud_quiz.delete_quiz(company_id=company_id, quiz_id_in_company=quiz_id)


@router.patch("/company/{company_id}/quiz/{quiz_id}/questions", status_code=200)
async def delete_questions(company_id: int, quiz_id: int, questions: quiz_schemas.DeleteQuestions, db: Database = Depends(get_sql_db), user: user_schemas.User = Depends(get_current_user)):
    crud_company = CompanyCrud(db=db)
    await crud_company.company_exists(company_id=company_id)
    crud_member = MemberCrud(db=db)
    member = await crud_member.get_member(company_id=company_id, user_id=user.id)
    if not member or member.role not in ["owner", "admin"]:
        raise HTTPException(status_code=403, detail="You are not allowed to delete questions")
    crud_quiz = QuizCrud(db=db)
    return await crud_quiz.delete_questions(company_id=company_id, quiz_id_in_company=quiz_id, questions=questions)
