from schemas import invite_schemas
from db import models
from databases import Database
import datetime
from fastapi import HTTPException, status
from sqlalchemy import insert, select, delete, update
from typing import List
from app.services.crud_member import MemberCrud
from app.services.crud_user import UserCrud
from app.services.crud_company import CompanyCrud


class InviteCrud:
    def __init__(self, db: Database):
        self.db = db

    async def invite_exists(self, invite_id: int) -> invite_schemas.Invite:
        invite_exists = await self.db.fetch_one(select(models.Invite).filter_by(invite_id=invite_id))
        if not invite_exists:
            raise HTTPException(status_code=404, detail="Invite not found")
        return invite_exists

    async def company_exists(self, company_id: int):
        company_exists = await self.db.fetch_one(select(models.Company).filter_by(company_id=company_id))
        if not company_exists:
            raise HTTPException(status_code=404, detail="Company does not exist")

    async def user_exists(self, user_id: int):
        user_exists = await self.db.fetch_one(select(models.User).filter_by(id=user_id))
        if not user_exists:
            raise HTTPException(status_code=404, detail="This user not found")

    async def get_invite(self, invite_id: int) -> invite_schemas.Invite:
        invite = await self.invite_exists(invite_id=invite_id)
        return invite

    async def get_all_invites(self, user_id: int | None = None, company_id: int | None = None) -> List[invite_schemas.Invite]:
        if user_id is None:
            await self.company_exists(company_id=company_id)
            result = await self.db.fetch_all(select(models.Invite).filter_by(from_company_id=company_id))
        else:
            result = await self.db.fetch_all(select(models.Invite).filter_by(to_user_id=user_id, status=None))
        return result

    async def create_invite(self, create_invite_form: invite_schemas.CreateInvite) -> HTTPException:
        await self.company_exists(company_id=create_invite_form.from_company_id)
        await self.user_exists(user_id=create_invite_form.to_user_id)
        payload = {
            "created_on": str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            "updated_on": str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            "to_user_id": create_invite_form.to_user_id,
            "from_company_id": create_invite_form.from_company_id,
            "invite_message": create_invite_form.invite_message,
        }
        query = insert(models.Invite).values(**payload)
        await self.db.execute(query=query)
        return HTTPException(status_code=200, detail="success")

    async def update_invite(self, invite_id: int, status_upd: str) -> HTTPException:
        invite = await self.invite_exists(invite_id=invite_id)
        if invite.status is not None:
            raise HTTPException(status_code=404, detail="User does not have an invite from the company")
        values = {"status": status_upd, "updated_on": str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))}
        await self.db.execute(update(models.Invite).filter_by(invite_id=invite_id), values=values)
        if status_upd == "ACCEPTED":
            crud_user = UserCrud(db=self.db)
            crud_member = MemberCrud(db=self.db)
            crud_company = CompanyCrud(db=self.db)
            user = await crud_user.get_user(user_id=invite.to_user_id)
            company = await crud_company.company_exists(company_id=invite.from_company_id)
            await crud_member.create_member(user_id=user.id, company_id=company.company_id)
        return HTTPException(status_code=200, detail="success")

    async def delete_invite(self, invite_id: int) -> status.HTTP_200_OK:
        await self.invite_exists(invite_id=invite_id)
        await self.db.execute(delete(models.Invite).filter_by(invite_id=invite_id))
        return HTTPException(status_code=200, detail="success")
