from databases import Database
from app.schemas import invite_schemas, user_schemas
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination import Page, paginate
from typing import List
from app.services.crud_company import CompanyCrud
from app.services.crud_invite import InviteCrud
from app.core.db_config import get_sql_db
from app.core.authorisation import get_current_user

router = APIRouter()


@router.get("/invite/my", response_model=Page[invite_schemas.Invite])
async def get_my_invites(db: Database = Depends(get_sql_db), user: user_schemas.User = Depends(get_current_user)) -> List[invite_schemas.Invite]:
    crud_invite = InviteCrud(db=db)
    invites = await crud_invite.get_all_invites(user_id=user.id)
    return paginate(invites)


@router.get("/invite/company/{company_id}", response_model=Page[invite_schemas.Invite])
async def get_company_invites(company_id: int, db: Database = Depends(get_sql_db), user: user_schemas.User = Depends(get_current_user)) -> List[invite_schemas.Invite]:
    crud_invite = InviteCrud(db=db)
    crud_company = CompanyCrud(db=db)
    company = await crud_company.get_company(company_id=company_id, user_id=user.id)
    owner_id = company.company_owner_id
    if user.id != owner_id:
        raise HTTPException(status_code=403, detail="It's not your company")
    invites = await crud_invite.get_all_invites(company_id=company_id)
    return paginate(invites)


@router.post("/invite", status_code=200)
async def create_invite(create_invite_form: invite_schemas.CreateInvite, db: Database = Depends(get_sql_db), user: user_schemas.User = Depends(get_current_user)):
    crud_invite = InviteCrud(db=db)
    crud_company = CompanyCrud(db=db)
    company = await crud_company.get_company(company_id=create_invite_form.from_company_id, user_id=user.id)
    owner_id = company.company_owner_id
    if user.id != owner_id:
        raise HTTPException(status_code=403, detail="It's not your company")
    return await crud_invite.create_invite(create_invite_form=create_invite_form)


@router.get("/invite/{invite_id}/accept", status_code=200)
async def accept_invite(invite_id: int, db: Database = Depends(get_sql_db), user: user_schemas.User = Depends(get_current_user)):
    crud_invite = InviteCrud(db=db)
    invite_to_upd = await crud_invite.get_invite(invite_id=invite_id)
    to_user_id = invite_to_upd.to_user_id
    if user.id != to_user_id:
        raise HTTPException(status_code=403, detail="It is not your invite")
    return await crud_invite.update_invite(invite_id=invite_id, status_upd="ACCEPTED")


@router.get("/invite/{invite_id}/decline", status_code=200)
async def accept_invite(invite_id: int, db: Database = Depends(get_sql_db), user: user_schemas.User = Depends(get_current_user)):
    crud_invite = InviteCrud(db=db)
    invite_to_upd = await crud_invite.get_invite(invite_id=invite_id)
    to_user_id = invite_to_upd.to_user_id
    if user.id != to_user_id:
        raise HTTPException(status_code=403, detail="It is not your invite")
    return await crud_invite.update_invite(invite_id=invite_id, status_upd="DECLINED")


@router.delete("/invite/{invite_id}", status_code=200)
async def cancel_invite(invite_id: int, db: Database = Depends(get_sql_db), user: user_schemas.User = Depends(get_current_user)):
    crud_invite = InviteCrud(db=db)
    crud_company = CompanyCrud(db=db)
    invite_record = await crud_invite.get_invite(invite_id=invite_id)
    company = await crud_company.get_company(company_id=invite_record.from_company_id, user_id=user.id)
    owner_id = company.company_owner_id
    if user.id != owner_id:
        raise HTTPException(status_code=403, detail="It's not your company")
    return await crud_invite.delete_invite(invite_id=invite_id)
