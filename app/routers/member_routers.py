from databases import Database
from app.schemas import member_schemas, user_schemas
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination import Page, paginate
from app.services.crud_company import CompanyCrud
from app.services.crud_member import MemberCrud
from app.core.db_config import get_sql_db
from app.core.authorisation import get_current_user

router = APIRouter()


@router.get("/company/{company_id}/members", response_model=Page[member_schemas.Member])
async def get_company_members(company_id: int, db: Database = Depends(get_sql_db), user: user_schemas.User = Depends(get_current_user)) -> Page[member_schemas.Member]:
    crud_member = MemberCrud(db=db)
    members = await crud_member.get_all_members(company_id=company_id)
    return paginate(members)


@router.get("/company/{company_id}/admins", response_model=Page[member_schemas.Member])
async def get_company_admins(company_id: int, db: Database = Depends(get_sql_db), user: user_schemas.User = Depends(get_current_user)) -> Page[member_schemas.Member]:
    crud_member = MemberCrud(db=db)
    crud_company = CompanyCrud(db=db)
    await crud_company.company_exists(company_id=company_id)
    members = await crud_member.get_all_admins(company_id=company_id)
    return paginate(members)


@router.post("/company/{company_id}/admin", status_code=200)
async def set_company_admin(company_id: int, admin_form: member_schemas.Admin, db: Database = Depends(get_sql_db), user: user_schemas.User = Depends(get_current_user)):
    crud_company = CompanyCrud(db=db)
    company = await crud_company.get_company(company_id=company_id, user_id=user.id)
    if user.id != company.company_owner_id:
        raise HTTPException(status_code=403, detail="It's not your company")
    crud_member = MemberCrud(db=db)
    return await crud_member.set_remove_admin(company_member_id=admin_form.company_member_id, company_id=company_id)


@router.delete("/company/{company_id}/member/{member_id}", status_code=200)
async def kick_member(company_id: int, member_id: int, db: Database = Depends(get_sql_db), user: user_schemas.User = Depends(get_current_user)):
    crud_member = MemberCrud(db=db)
    crud_company = CompanyCrud(db=db)
    company = await crud_company.get_company(company_id=company_id, user_id=user.id)
    if user.id != company.company_owner_id:
        raise HTTPException(status_code=403, detail="It's not your company")
    return await crud_member.delete_member(company_member_id=member_id, company_id=company_id)


@router.delete("/company/{company_id}/leave", status_code=200)
async def leave_company(company_id: int, db: Database = Depends(get_sql_db), user: user_schemas.User = Depends(get_current_user)):
    crud_member = MemberCrud(db=db)
    return await crud_member.delete_member(company_id=company_id, user_id=user.id)


@router.delete("/company/{company_id}/admin/{member_id}", status_code=200)
async def remove_admin(company_id: int, member_id: int, db: Database = Depends(get_sql_db), user: user_schemas.User = Depends(get_current_user)):
    crud_member = MemberCrud(db=db)
    crud_company = CompanyCrud(db=db)
    company = await crud_company.get_company(company_id=company_id, user_id=user.id)
    if user.id != company.company_owner_id:
        raise HTTPException(status_code=403, detail="It's not your company")
    return await crud_member.set_remove_admin(company_member_id=member_id, company_id=company_id)
