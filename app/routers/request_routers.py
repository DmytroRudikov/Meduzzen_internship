import sys
import os
sys.path.append(os.getcwd())

from databases import Database
from app.schemas import request_schemas, user_schemas
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination import Page, paginate
from typing import List
from app.services.crud_company import CompanyCrud
from app.services.crud_request import RequestCrud
from app.core.db_config import get_sql_db
from app.core.authorisation import get_current_user

router = APIRouter()


@router.get("/request/my", response_model=Page[request_schemas.Request])
async def get_my_requests(db: Database = Depends(get_sql_db), user: user_schemas.User = Depends(get_current_user)) -> List[request_schemas.Request]:
    crud_request = RequestCrud(db=db)
    requests = await crud_request.get_all_requests(user_id=user.id)
    return paginate(requests)


@router.get("/request/company/{company_id}", response_model=Page[request_schemas.Request])
async def get_company_requests(company_id: int, db: Database = Depends(get_sql_db), user: user_schemas.User = Depends(get_current_user)) -> List[request_schemas.Request]:
    crud_request = RequestCrud(db=db)
    crud_company = CompanyCrud(db=db)
    company = await crud_company.get_company(company_id=company_id, user_id=user.id)
    owner_id = company.company_owner_id
    if user.id != owner_id:
        raise HTTPException(status_code=403, detail="It's not your company")
    requests = await crud_request.get_all_requests(company_id=company_id)
    return paginate(requests)


@router.post("/request", status_code=200)
async def create_request(create_request_form: request_schemas.CreateRequest, db: Database = Depends(get_sql_db), user: user_schemas.User = Depends(get_current_user)):
    crud_request = RequestCrud(db=db)
    return await crud_request.create_request(create_request_form=create_request_form, user_id=user.id)


@router.get("/request/{request_id}/accept", status_code=200)
async def accept_request(request_id: int, db: Database = Depends(get_sql_db), user: user_schemas.User = Depends(get_current_user)):
    crud_request = RequestCrud(db=db)
    crud_company = CompanyCrud(db=db)
    request_to_upd = await crud_request.get_request(request_id=request_id)
    company = await crud_company.get_company(company_id=request_to_upd.to_company_id, user_id=user.id)
    if user.id != company.company_owner_id:
        raise HTTPException(status_code=403, detail="Only the owner of the company can accept requests")
    return await crud_request.update_request(request_id=request_id, status_upd="ACCEPTED")


@router.get("/request/{request_id}/decline", status_code=200)
async def decline_request(request_id: int, db: Database = Depends(get_sql_db), user: user_schemas.User = Depends(get_current_user)):
    crud_request = RequestCrud(db=db)
    crud_company = CompanyCrud(db=db)
    request_to_upd = await crud_request.get_request(request_id=request_id)
    company = await crud_company.get_company(company_id=request_to_upd.to_company_id, user_id=user.id)
    if user.id != company.company_owner_id:
        raise HTTPException(status_code=403, detail="Only the owner of the company can decline requests")
    return await crud_request.update_request(request_id=request_id, status_upd="DECLINED")


@router.delete("/request/{request_id}", status_code=200)
async def cancel_request(request_id: int, db: Database = Depends(get_sql_db), user: user_schemas.User = Depends(get_current_user)):
    crud_request = RequestCrud(db=db)
    request_record = await crud_request.get_request(request_id=request_id)
    if user.id != request_record.from_user_id:
        raise HTTPException(status_code=403, detail="It's not your request")
    return await crud_request.delete_request(request_id=request_id)
