from databases import Database
from fastapi import APIRouter, Depends, HTTPException
from app.schemas import user_schemas
from app.services.crud_company import CompanyCrud
from app.services.crud_member import MemberCrud
from app.services.crud_quiz import QuizCrud
from app.core.db_config import get_sql_db
from app.core.authorisation import get_current_user
from app.services.export_redis_data import ExportRedis
from typing import TextIO

router = APIRouter()


@router.get("/my_results/export/json", response_model=None)
async def export_user_results_json(user: user_schemas.User = Depends(get_current_user)) -> TextIO:
    crud_redis = ExportRedis()
    results = await crud_redis.redis_export_json_all_user_results(user_id=user.id)
    return results


@router.get("/my_results/export/csv", response_model=None)
async def export_user_results_json(user: user_schemas.User = Depends(get_current_user)) -> TextIO:
    crud_redis = ExportRedis()
    results = await crud_redis.redis_export_csv_all_user_results(user_id=user.id)
    return results


@router.get("/company/{company_id}/results/export/json", response_model=None)
async def export_all_company_results_json(company_id: int, db: Database = Depends(get_sql_db), user: user_schemas.User = Depends(get_current_user)) -> TextIO:
    crud_company = CompanyCrud(db=db)
    await crud_company.company_exists(company_id=company_id)
    crud_member = MemberCrud(db=db)
    member_role = await crud_member.get_member(company_id=company_id, user_id=user.id)
    if not member_role or member_role.role not in ["owner", "admin"]:
        raise HTTPException(status_code=403, detail="You are not allowed to export results")
    crud_redis = ExportRedis()
    results = await crud_redis.redis_export_json_all_company_members_results(company_id=company_id)
    return results


@router.get("/company/{company_id}/results/export/csv", response_model=None)
async def export_all_company_results_csv(company_id: int, db: Database = Depends(get_sql_db), user: user_schemas.User = Depends(get_current_user)) -> TextIO:
    crud_company = CompanyCrud(db=db)
    await crud_company.company_exists(company_id=company_id)
    crud_member = MemberCrud(db=db)
    member_role = await crud_member.get_member(company_id=company_id, user_id=user.id)
    if not member_role or member_role.role not in ["owner", "admin"]:
        raise HTTPException(status_code=403, detail="You are not allowed to export results")
    crud_redis = ExportRedis()
    results = await crud_redis.redis_export_csv_all_company_members_results(company_id=company_id)
    return results


@router.get("/company/{company_id}/member/{member_id}/results/export/json", response_model=None)
async def export_company_member_results_json(company_id: int, member_id: int, db: Database = Depends(get_sql_db), user: user_schemas.User = Depends(get_current_user)) -> TextIO:
    crud_company = CompanyCrud(db=db)
    await crud_company.company_exists(company_id=company_id)
    crud_member = MemberCrud(db=db)
    member_exists = await crud_member.member_exists(company_id=company_id, company_member_id=member_id)
    member_role = await crud_member.get_member(company_id=company_id, user_id=user.id)
    if not member_role or member_role.role not in ["owner", "admin"]:
        raise HTTPException(status_code=403, detail="You are not allowed to export results")
    crud_redis = ExportRedis()
    results = await crud_redis.redis_export_json_one_company_member_results(company_id=company_id, user_id=member_exists.user_id)
    return results


@router.get("/company/{company_id}/member/{member_id}/results/export/csv", response_model=None)
async def export_company_member_results_csv(company_id: int, member_id: int, db: Database = Depends(get_sql_db), user: user_schemas.User = Depends(get_current_user)) -> TextIO:
    crud_company = CompanyCrud(db=db)
    await crud_company.company_exists(company_id=company_id)
    crud_member = MemberCrud(db=db)
    member_exists = await crud_member.member_exists(company_id=company_id, company_member_id=member_id)
    member_role = await crud_member.get_member(company_id=company_id, user_id=user.id)
    if not member_role or member_role.role not in ["owner", "admin"]:
        raise HTTPException(status_code=403, detail="You are not allowed to export results")
    crud_redis = ExportRedis()
    results = await crud_redis.redis_export_csv_one_company_member_results(company_id=company_id, user_id=member_exists.user_id)
    return results


@router.get("/company/{company_id}/quiz/{quiz_id}/results/export/json", response_model=None)
async def export_all_results_by_company_for_quiz_specified_json(company_id: int, quiz_id: int, db: Database = Depends(get_sql_db), user: user_schemas.User = Depends(get_current_user)) -> TextIO:
    crud_company = CompanyCrud(db=db)
    await crud_company.company_exists(company_id=company_id)
    crud_member = MemberCrud(db=db)
    member = await crud_member.get_member(company_id=company_id, user_id=user.id)
    if not member or member.role not in ["owner", "admin"]:
        raise HTTPException(status_code=403, detail="You are not allowed to export results")
    crud_quiz = QuizCrud(db=db)
    await crud_quiz.quiz_exists(quiz_id_in_company=quiz_id, company_id=company_id)
    crud_redis = ExportRedis()
    results = await crud_redis.redis_export_json_results_for_one_quiz_in_company(company_id=company_id, quiz_id_in_company=quiz_id)
    return results


@router.get("/company/{company_id}/quiz/{quiz_id}/results/export/csv", response_model=None)
async def export_all_results_by_company_for_quiz_specified_csv(company_id: int, quiz_id: int, db: Database = Depends(get_sql_db), user: user_schemas.User = Depends(get_current_user)) -> TextIO:
    crud_company = CompanyCrud(db=db)
    await crud_company.company_exists(company_id=company_id)
    crud_member = MemberCrud(db=db)
    member = await crud_member.get_member(company_id=company_id, user_id=user.id)
    if not member or member.role not in ["owner", "admin"]:
        raise HTTPException(status_code=403, detail="You are not allowed to export results")
    crud_quiz = QuizCrud(db=db)
    await crud_quiz.quiz_exists(quiz_id_in_company=quiz_id, company_id=company_id)
    crud_redis = ExportRedis()
    results = await crud_redis.redis_export_csv_results_for_one_quiz_in_company(company_id=company_id, quiz_id_in_company=quiz_id)
    return results
