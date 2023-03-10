from schemas import schemas
from db import models
from core.db_config import get_sql_db
from databases import Database
from passlib.context import CryptContext
import datetime
from fastapi import HTTPException, status, Depends
from sqlalchemy import insert, select, delete, update

context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserCrud:
    def __init__(self, db: Database = Depends(get_sql_db)):
        self.db = db

    async def user_exists(self, user_id=None, email=None):
        if user_id is None:
            user_exists = await self.db.fetch_one(select(models.User).filter_by(email=email))
            if user_exists:
                raise HTTPException(status_code=400, detail="User with this email already exists")
        elif email is None:
            user_exists = await self.db.fetch_one(select(models.User).filter_by(id=user_id))
            if not user_exists:
                raise HTTPException(status_code=404, detail="User with this id does not exist")
            return user_exists

    async def get_user(self, user_id: int) -> schemas.User:
        user = await self.user_exists(user_id=user_id)
        return user

    async def get_all_users(self) -> list:
        result = await self.db.fetch_all(select(models.User))
        return result

    async def create_user(self, signup_form: schemas.SignupRequest) -> schemas.User:
        await self.user_exists(email=signup_form.email)
        hashed_password = context.hash(signup_form.password)
        created_on = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        updated_on = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        form_dict = signup_form.dict()
        form_dict["password"] = hashed_password
        form_dict["created_on"] = created_on
        form_dict["updated_on"] = updated_on
        form_dict.pop("password_check")
        query = insert(models.User).values(**form_dict)
        await self.db.execute(query=query)
        new_user = await self.db.fetch_one(select(models.User).filter_by(email=form_dict.get("email")))
        return new_user

    async def update_user_details(self, user: schemas.User, user_id: int, user_upd: schemas.UserUpdate):
        for key in user._mapping.keys():
            if key == "updated_on":
                await self.db.execute(update(models.User).filter_by(id=user_id).values(
                    updated_on=str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))))
            elif key not in user_upd.dict() or user_upd.dict()[key] is None:
                continue
            else:
                await self.db.execute(update(models.User).filter_by(id=user_id), values={key: user_upd.dict()[key]})

    async def update_user(self, user_id: int, user_upd: schemas.UserUpdate) -> schemas.User:
        user = await self.user_exists(user_id=user_id)
        await self.update_user_details(user=user, user_upd=user_upd, user_id=user_id)
        updated_user = await self.db.fetch_one(select(models.User).filter_by(id=user_id))
        return updated_user

    async def delete_user(self, user_id: int):
        await self.db.execute(delete(models.User).filter_by(id=user_id))
        return status.HTTP_200_OK
