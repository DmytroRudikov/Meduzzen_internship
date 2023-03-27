from schemas import member_schemas
from db import models
from databases import Database
import datetime
from fastapi import HTTPException, status
from sqlalchemy import insert, select, delete, update
from typing import List


class MemberCrud:
    def __init__(self, db: Database):
        self.db = db

    async def check_the_last_company_member_id(self, company_id: int) -> int:
        last_company_member = await self.db.fetch_one(select(models.MemberRecord).filter_by(company_id=company_id).order_by(models.MemberRecord.company_member_id.desc()))
        if last_company_member:
            last_company_member_id = last_company_member.company_member_id
        else:
            last_company_member_id = 0
        return last_company_member_id

    async def create_member(self, user_id: int, company_id: int):
        last_company_member_id = await self.check_the_last_company_member_id(company_id=company_id)
        last_company_member_id += 1
        values = {
            "user_id": user_id,
            "company_id": company_id,
            "created_on": str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            "updated_on": str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            "company_member_id": last_company_member_id
        }
        await self.db.execute(insert(models.MemberRecord), values=values)

    async def get_member(self, company_id: int, company_member_id: int | None = None, user_id: int | None = None) -> member_schemas.Member:
        if user_id is None:
            member = await self.db.fetch_one(select(models.MemberRecord).filter_by(company_id=company_id, company_member_id=company_member_id))
        else:
            member = await self.db.fetch_one(
                select(models.MemberRecord).filter_by(company_id=company_id, user_id=user_id)
            )
        return member

    async def get_all_members(self, company_id: int) -> List[member_schemas.Member]:
        result = await self.db.fetch_all(select(models.MemberRecord).filter_by(company_id=company_id))
        return result

    async def update_member(self):
        pass

    async def delete_member(self, company_id: int, company_member_id: int | None = None, user_id: int | None = None) -> status.HTTP_200_OK:
        if user_id is None:
            await self.db.execute(delete(models.MemberRecord).filter_by(company_member_id=company_member_id, company_id=company_id))
        else:
            await self.db.execute(
                delete(models.MemberRecord).filter_by(user_id=user_id, company_id=company_id)
            )
        return HTTPException(status_code=200)
