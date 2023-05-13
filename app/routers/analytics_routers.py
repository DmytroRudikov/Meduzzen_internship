import sys
import os
sys.path.append(os.getcwd())

from databases import Database
from app.schemas import member_schemas, user_schemas, quiz_schemas, results_schemas, analytics_schemas
from fastapi import APIRouter, Depends, HTTPException, status
from app.services.crud_user import UserCrud
from app.services.crud_company import CompanyCrud
from app.services.crud_member import MemberCrud
from app.services.crud_quiz import QuizCrud
from app.services.crud_results import ResultsCrud
from app.services.analytics_crud import AnalyticsCrud
from app.core.db_config import get_sql_db
from app.core.authorisation import get_current_user
from typing import List

router = APIRouter()


@router.get("/my_average_result", status_code=200)
async def get_my_average_result(db: Database = Depends(get_sql_db), user: user_schemas.User = Depends(get_current_user)) -> float:
    crud_analytics = AnalyticsCrud(db=db)
    result = await crud_analytics.get_my_average_result(user_id=user.id)
    return result


@router.get("/my_average_results", response_model=List[analytics_schemas.MyResults])
async def get_my_average_results(db: Database = Depends(get_sql_db), user: user_schemas.User = Depends(get_current_user)) -> List[analytics_schemas.MyResults]:
    crud_analytics = AnalyticsCrud(db=db)
    results = await crud_analytics.get_list_my_average_results(user_id=user.id)
    return results


@router.get("/my_quizzes_passed", response_model=List[analytics_schemas.QuizzesList])
async def get_quizzes_passed(db: Database = Depends(get_sql_db), user: user_schemas.User = Depends(get_current_user)) -> List[analytics_schemas.QuizzesList]:
    crud_analytics = AnalyticsCrud(db=db)
    results = await crud_analytics.get_list_of_quizzes_passed(user_id=user.id)
    return results


@router.get("/company/{company_id}/members/results", response_model=List[analytics_schemas.MemberResults])
async def get_all_members_results(company_id: int, db: Database = Depends(get_sql_db), user: user_schemas.User = Depends(get_current_user)) -> List[analytics_schemas.MemberResults]:
    crud_company = CompanyCrud(db=db)
    await crud_company.company_exists(company_id=company_id)
    crud_member = MemberCrud(db=db)
    member_role = await crud_member.get_member(company_id=company_id, user_id=user.id)
    if not member_role or member_role.role not in ["owner", "admin"]:
        raise HTTPException(status_code=403, detail="You are not allowed to see results")
    crud_analytics = AnalyticsCrud(db=db)
    results = await crud_analytics.get_list_all_members_results(company_id=company_id)
    return results


@router.get("/company/{company_id}/member/{member_id}/results", response_model=List[analytics_schemas.MemberResults])
async def get_all_results_for_specific_member(company_id: int, member_id: int, db: Database = Depends(get_sql_db), user: user_schemas.User = Depends(get_current_user)) -> List[analytics_schemas.MemberResults]:
    crud_company = CompanyCrud(db=db)
    await crud_company.company_exists(company_id=company_id)
    crud_member = MemberCrud(db=db)
    member_exists = await crud_member.member_exists(company_id=company_id, company_member_id=member_id)
    member_role = await crud_member.get_member(company_id=company_id, user_id=user.id)
    if not member_role or member_role.role not in ["owner", "admin"]:
        raise HTTPException(status_code=403, detail="You are not allowed to see results")
    crud_analytics = AnalyticsCrud(db=db)
    results = await crud_analytics.get_all_results_for_specific_member(company_id=company_id, user_id=member_exists.user_id)
    return results


@router.get("/company/{company_id}/members_passed", response_model=List[analytics_schemas.MembersPassed])
async def get_list_of_members_passed(company_id: int, db: Database = Depends(get_sql_db), user: user_schemas.User = Depends(get_current_user)) -> List[analytics_schemas.MembersPassed]:
    crud_company = CompanyCrud(db=db)
    await crud_company.company_exists(company_id=company_id)
    crud_member = MemberCrud(db=db)
    member_role = await crud_member.get_member(company_id=company_id, user_id=user.id)
    if not member_role or member_role.role not in ["owner", "admin"]:
        raise HTTPException(status_code=403, detail="You are not allowed to see results")
    crud_analytics = AnalyticsCrud(db=db)
    results = await crud_analytics.get_list_of_members_passed(company_id=company_id)
    return results
