import sys
import os
sys.path.append(os.getcwd())

from databases import Database
from app.schemas import member_schemas, user_schemas, quiz_schemas, results_schemas
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination import Page, paginate
from app.services.crud_user import UserCrud
from app.services.crud_company import CompanyCrud
from app.services.crud_member import MemberCrud
from app.services.crud_quiz import QuizCrud
from app.services.crud_results import ResultsCrud
from app.core.db_config import get_sql_db
from app.core.authorisation import get_current_user
from typing import List

router = APIRouter()


@router.post("/company/{company_id}/quiz/{quiz_id}/send_answers", status_code=200)
async def send_answers_for_the_quiz(company_id: int, quiz_id: int, answers: results_schemas.AnswerQuiz, db: Database = Depends(get_sql_db), user: user_schemas.User = Depends(get_current_user)):
    crud_company = CompanyCrud(db=db)
    await crud_company.company_exists(company_id=company_id)
    crud_member = MemberCrud(db=db)
    member = await crud_member.get_member(company_id=company_id, user_id=user.id)
    if not member:
        raise HTTPException(status_code=403, detail="You are not a member to take the quiz")
    crud_results = ResultsCrud(db=db)
    return await crud_results.record_results(answers=answers, company_id=company_id, quiz_id_in_company=quiz_id, user_id=user.id)


@router.get("/quizzes/my_results", response_model=Page[results_schemas.Results])
async def get_user_results(db: Database = Depends(get_sql_db), user: user_schemas.User = Depends(get_current_user)) -> Page[results_schemas.Results]:
    crud_results = ResultsCrud(db=db)
    results = await crud_results.get_all_user_results(user_id=user.id)
    return paginate(results)


@router.get("/company/{company_id}/member/{member_id}/quizzes/results", response_model=Page[results_schemas.Results])
async def get_company_member_results(company_id: int, member_id: int, db: Database = Depends(get_sql_db), user: user_schemas.User = Depends(get_current_user)) -> Page[results_schemas.Results]:
    crud_company = CompanyCrud(db=db)
    await crud_company.company_exists(company_id=company_id)
    crud_member = MemberCrud(db=db)
    member_exists = await crud_member.member_exists(company_id=company_id, company_member_id=member_id)
    member_role = await crud_member.get_member(company_id=company_id, user_id=user.id)
    if member_exists.user_id != user.id:
        if not member_role or member_role.role not in ["owner", "admin"]:
            raise HTTPException(status_code=403, detail="You are not allowed to see results")
    crud_results = ResultsCrud(db=db)
    results = await crud_results.get_all_company_member_results(user_id=member_exists.user_id, company_id=company_id)
    return paginate(results)


@router.get("/company/{company_id}/member/{member_id}/quiz/{quiz_id}/results", response_model=Page[results_schemas.Results])
async def get_company_member_results_by_quiz(company_id: int, quiz_id: int, member_id: int, db: Database = Depends(get_sql_db), user: user_schemas.User = Depends(get_current_user)) -> Page[results_schemas.Results]:
    crud_company = CompanyCrud(db=db)
    await crud_company.company_exists(company_id=company_id)
    crud_member = MemberCrud(db=db)
    member_exists = await crud_member.member_exists(company_id=company_id, company_member_id=member_id)
    member_role = await crud_member.get_member(company_id=company_id, user_id=user.id)
    if member_exists.user_id != user.id:
        if not member_role or member_role.role not in ["owner", "admin"]:
            raise HTTPException(status_code=403, detail="You are not allowed to see results")
    crud_results = ResultsCrud(db=db)
    results = await crud_results.get_company_member_results_by_quiz(user_id=member_exists.user_id, company_id=company_id, quiz_id_in_company=quiz_id)
    return paginate(results)


@router.get("/company/{company_id}/quizzes/results", response_model=Page[results_schemas.Results])
async def get_all_results_by_company(company_id: int, db: Database = Depends(get_sql_db), user: user_schemas.User = Depends(get_current_user)) -> Page[results_schemas.Results]:
    crud_company = CompanyCrud(db=db)
    await crud_company.company_exists(company_id=company_id)
    crud_member = MemberCrud(db=db)
    member = await crud_member.get_member(company_id=company_id, user_id=user.id)
    if not member or member.role not in ["owner", "admin"]:
        raise HTTPException(status_code=403, detail="You are not allowed to see results")
    crud_results = ResultsCrud(db=db)
    results = await crud_results.get_all_results_by_company(company_id=company_id)
    return paginate(results)


@router.get("/company/{company_id}/quiz/{quiz_id}/results", response_model=Page[results_schemas.Results])
async def get_all_results_by_company_for_quiz_specified(company_id: int, quiz_id: int, db: Database = Depends(get_sql_db), user: user_schemas.User = Depends(get_current_user)) -> Page[results_schemas.Results]:
    crud_company = CompanyCrud(db=db)
    await crud_company.company_exists(company_id=company_id)
    crud_member = MemberCrud(db=db)
    member = await crud_member.get_member(company_id=company_id, user_id=user.id)
    if not member or member.role not in ["owner", "admin"]:
        raise HTTPException(status_code=403, detail="You are not allowed to see results")
    crud_results = ResultsCrud(db=db)
    results = await crud_results.get_all_results_by_company_for_quiz_specified(company_id=company_id, quiz_id_in_company=quiz_id)
    return paginate(results)


@router.get("/company/{company_id}/member/{member_id}/average_result", status_code=200)
async def get_average_result_for_company_member(company_id: int, member_id: int, db: Database = Depends(get_sql_db), user: user_schemas.User = Depends(get_current_user)) -> float:
    crud_company = CompanyCrud(db=db)
    await crud_company.company_exists(company_id=company_id)
    crud_member = MemberCrud(db=db)
    member_exists = await crud_member.member_exists(company_id=company_id, company_member_id=member_id)
    member_role = await crud_member.get_member(company_id=company_id, user_id=user.id)
    if member_exists.user_id != user.id:
        if not member_role or member_role.role not in ["owner", "admin"]:
            raise HTTPException(status_code=403, detail="You are not allowed to see results")
    crud_results = ResultsCrud(db=db)
    average_result = await crud_results.average_result_for_company_member(company_id=company_id, user_id=member_exists.user_id)
    return average_result


@router.get("/user/{user_id}/average_result", status_code=200)
async def get_average_result_for_user_in_the_system(user_id: int, db: Database = Depends(get_sql_db), user: user_schemas.User = Depends(get_current_user)) -> float:
    crud_user = UserCrud(db=db)
    await crud_user.user_exists(user_id=user_id)
    crud_results = ResultsCrud(db=db)
    average_result = await crud_results.average_result_for_user_in_the_system(user_id=user_id)
    return average_result
