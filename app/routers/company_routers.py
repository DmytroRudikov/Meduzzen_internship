import sys
import os
sys.path.append(os.getcwd())

from databases import Database
from app.schemas import company_schemas, user_schemas
from fastapi import APIRouter, Depends, HTTPException
from fastapi_pagination import Page, paginate
from typing import List
from app.services.crud_user import UserCrud
from app.services.crud_company import CompanyCrud
from app.core.db_config import get_sql_db
from app.core.authorisation import Auth, get_current_user

router = APIRouter()


@router.get("/company/{company_id}", response_model=company_schemas.Company)
async def get_company(company_id: int, db: Database = Depends(get_sql_db), user: user_schemas.User = Depends(get_current_user)) -> company_schemas.Company:
    crud_company = CompanyCrud(db=db)
    return await crud_company.get_company(company_id=company_id, user_id=user.id)


@router.get("/companies", response_model=Page[company_schemas.Company])
async def get_all_companies(db: Database = Depends(get_sql_db), user: user_schemas.User = Depends(get_current_user)) -> List[company_schemas.Company]:
    crud_company = CompanyCrud(db=db)
    companies = await crud_company.get_all_companies(user_id=user.id)
    return paginate(companies)


@router.post("/company", response_model=company_schemas.Company, status_code=201)
async def create_company(create_company_form: company_schemas.CreateCompany, db: Database = Depends(get_sql_db), user: user_schemas.User = Depends(get_current_user)) -> company_schemas.Company:
    crud_company = CompanyCrud(db=db)
    return await crud_company.create_company(create_company_form=create_company_form, user_id=user.id)


@router.put("/company/{company_id}", response_model=company_schemas.Company)
async def update_company(company_upd: company_schemas.CompanyUpdate, company_id: int, db: Database = Depends(get_sql_db), user: user_schemas.User = Depends(get_current_user)) -> company_schemas.Company:
    crud_company = CompanyCrud(db=db)
    comp_to_upd = await crud_company.get_company(company_id=company_id, user_id=user.id)
    owner_id = comp_to_upd.company_owner_id
    if user.id != owner_id:
        raise HTTPException(status_code=403, detail="It's not your company")
    return await crud_company.update_company(company_id=company_id, company_upd=company_upd)


@router.delete("/company/{company_id}", status_code=200)
async def delete_company(company_id: int, db: Database = Depends(get_sql_db), user: user_schemas.User = Depends(get_current_user)):
    crud_company = CompanyCrud(db=db)
    comp_to_delete = await crud_company.get_company(company_id=company_id, user_id=user.id)
    owner_id = comp_to_delete.company_owner_id
    if user.id != owner_id:
        raise HTTPException(status_code=403, detail="It's not your company")
    return await crud_company.delete_company(company_id=company_id)
