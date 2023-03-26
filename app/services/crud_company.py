from schemas import company_schemas
from db import models
from databases import Database
import datetime
from fastapi import HTTPException, status
from sqlalchemy import insert, select, delete, update
from typing import List
from app.services.crud_user import UserCrud
from app.services.crud_member import MemberCrud
from app.core.db_config import get_sql_db


class CompanyCrud:
    def __init__(self, db: Database):
        self.db = db

    async def company_exists(self, company_id=None, company_name=None) -> company_schemas.Company:
        if company_id is None:
            company_exists = await self.db.fetch_one(select(models.Company).filter_by(company_name=company_name))
            if company_exists:
                raise HTTPException(status_code=400, detail="Company with this name already exists")
        elif company_name is None:
            company_exists = await self.db.fetch_one(select(models.Company).filter_by(company_id=company_id))
            if not company_exists:
                raise HTTPException(status_code=404, detail="Company does not exist")
            return company_exists

    async def visibility_check(self, companies: list, user_id: int) -> List[company_schemas.Company]:
        companies_to_return = []
        crud_user = UserCrud(db=self.db)
        for comp in companies:
            if comp.company_visible is None or comp.company_visible:
                companies_to_return.append(comp)
            else:
                user = await crud_user.get_user(user_id=user_id)
                if user.id == comp.company_owner_id:
                    companies_to_return.append(comp)
                else:
                    if len(companies) == 1:
                        raise HTTPException(status_code=403, detail="The company is invisible")
        return companies_to_return

    async def get_company(self, company_id: int, user_id: int) -> company_schemas.Company:
        company = await self.company_exists(company_id=company_id)
        to_return_if_visible = await self.visibility_check([company], user_id=user_id)
        return to_return_if_visible[0]

    async def get_all_companies(self, user_id: int) -> List[company_schemas.Company]:
        result = await self.db.fetch_all(select(models.Company))
        to_return_if_visible = await self.visibility_check(result, user_id=user_id)
        return to_return_if_visible

    async def create_company(self, user_id: int, create_company_form: company_schemas.CreateCompany) -> company_schemas.Company:
        await self.company_exists(company_name=create_company_form.company_name)
        payload = {
            "created_on": str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            "updated_on": str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            "company_name": create_company_form.company_name,
            "company_description": create_company_form.company_description,
            "company_visible": create_company_form.company_visible,
            "company_owner_id": user_id
        }
        query = insert(models.Company).values(**payload)
        await self.db.execute(query=query)
        new_company = await self.db.fetch_one(select(models.Company).filter_by(company_name=payload.get("company_name")))
        crud_member = MemberCrud(db=self.db)
        await crud_member.create_member(user_id=user_id, company_id=new_company.company_id)
        return new_company

    @staticmethod
    async def update_company_details(company: company_schemas.Company, company_upd: company_schemas.CompanyUpdate) -> company_schemas.Company:
        updates = {}
        for key in company._mapping.keys():
            if key == "updated_on":
                updates["updated_on"] = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            elif key not in company_upd.dict() or company_upd.dict()[key] is None:
                continue
            else:
                updates[key] = company_upd.dict()[key]
        return updates

    async def update_company(self, company_id: int, company_upd: company_schemas.CompanyUpdate) -> company_schemas.Company:
        company = await self.company_exists(company_id=company_id)
        company_update_dict = await self.update_company_details(company=company, company_upd=company_upd)
        await self.db.execute(update(models.Company).filter_by(company_id=company_id), values=company_update_dict)
        updated_company = await self.db.fetch_one(select(models.Company).filter_by(company_id=company_id))
        return updated_company

    async def delete_company(self, company_id: int) -> status.HTTP_200_OK:
        await self.db.execute(delete(models.Company).filter_by(company_id=company_id))
        return status.HTTP_200_OK

