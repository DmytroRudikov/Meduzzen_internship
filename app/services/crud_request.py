from schemas import request_schemas
from db import models
from databases import Database
import datetime
from fastapi import HTTPException, status
from sqlalchemy import insert, select, delete, update
from typing import List
from app.services.crud_member import MemberCrud
from app.services.crud_company import CompanyCrud
from app.services.crud_user import UserCrud


class RequestCrud:
    def __init__(self, db: Database):
        self.db = db

    async def request_exists(self, request_id: int) -> request_schemas.Request:
        request_exists = await self.db.fetch_one(select(models.Request).filter_by(request_id=request_id))
        if not request_exists:
            raise HTTPException(status_code=404, detail="Request not found")
        return request_exists

    async def get_request(self, request_id: int) -> request_schemas.Request:
        request = await self.request_exists(request_id=request_id)
        return request

    async def get_all_requests(self, user_id: int | None = None, company_id: int | None = None) -> List[request_schemas.Request]:
        if user_id is None:
            crud_company = CompanyCrud(db=self.db)
            await crud_company.company_exists(company_id=company_id)
            result = await self.db.fetch_all(select(models.Request).filter_by(to_company_id=company_id, status=None))
        else:
            result = await self.db.fetch_all(select(models.Request).filter_by(from_user_id=user_id))
        return result

    async def create_request(self, create_request_form: request_schemas.CreateRequest, user_id: int) -> status.HTTP_200_OK:
        crud_company = CompanyCrud(db=self.db)
        await crud_company.company_exists(company_id=create_request_form.to_company_id)
        crud_member = MemberCrud(db=self.db)
        member_exists = await crud_member.get_member(user_id=user_id, company_id=create_request_form.to_company_id)
        if member_exists:
            raise HTTPException(status_code=400, detail="User is already a member of the company")
        request_sent = await self.db.fetch_one(select(models.Request).filter_by(from_user_id=user_id, to_company_id=create_request_form.to_company_id))
        if request_sent:
            raise HTTPException(status_code=400, detail="Request already sent")
        payload = {
            "created_on": str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            "updated_on": str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            "from_user_id": user_id,
            "to_company_id": create_request_form.to_company_id,
            "request_message": create_request_form.request_message,
        }
        query = insert(models.Request).values(**payload)
        await self.db.execute(query=query)
        return HTTPException(status_code=200, detail="success")

    async def update_request(self, request_id: int, status_upd: str) -> HTTPException:
        request = await self.request_exists(request_id=request_id)
        if request.status is not None:
            raise HTTPException(status_code=404, detail="Company does not have a request from the user")
        values = {"status": status_upd, "updated_on": str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))}
        await self.db.execute(update(models.Request).filter_by(request_id=request_id), values=values)
        if status_upd == "ACCEPTED":
            crud_user = UserCrud(db=self.db)
            crud_member = MemberCrud(db=self.db)
            crud_company = CompanyCrud(db=self.db)
            user = await crud_user.get_user(user_id=request.from_user_id)
            company = await crud_company.company_exists(company_id=request.to_company_id)
            await crud_member.create_member(user_id=user.id, company_id=company.company_id)
        return HTTPException(status_code=200, detail="success")

    async def delete_request(self, request_id: int) -> status.HTTP_200_OK:
        await self.request_exists(request_id=request_id)
        await self.db.execute(delete(models.Request).filter_by(request_id=request_id))
        return HTTPException(status_code=200, detail="success")
