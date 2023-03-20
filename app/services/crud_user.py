import os

from schemas import user_schemas
from db import models
from core.db_config import get_sql_db
from databases import Database
from passlib.context import CryptContext
import datetime
from fastapi import HTTPException, status
from sqlalchemy import insert, select, delete, update
from jose import jwt, JWTError
from typing import List

context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserCrud:
    def __init__(self, db: Database):
        self.db = db

    async def user_exists(self, user_id=None, email=None) -> user_schemas.User:
        if user_id is None:
            user_exists = await self.db.fetch_one(select(models.User).filter_by(email=email))
            if user_exists:
                raise HTTPException(status_code=400, detail="User with this email already exists")
        elif email is None:
            user_exists = await self.db.fetch_one(select(models.User).filter_by(id=user_id))
            if not user_exists:
                raise HTTPException(status_code=404, detail="User with this id does not exist")
            return user_exists

    async def user_exists_for_auth(self, email: str) -> user_schemas.User:
        user_exists = await self.db.fetch_one(select(models.User).filter_by(email=email))
        if not user_exists:
            raise HTTPException(status_code=401, detail="Incorrect username or password")
        return user_exists

    async def get_user(self, user_id: int, email=None) -> user_schemas.User:
        if email is None:
            user = await self.user_exists(user_id=user_id)
        else:
            user = await self.user_exists_for_auth(email=email)
        return user

    async def get_all_users(self) -> List[user_schemas.User]:
        result = await self.db.fetch_all(select(models.User))
        return result

    async def create_user(self, signup_form: user_schemas.SignupRequest) -> user_schemas.User:
        await self.user_exists(email=signup_form.email)
        hashed_password = context.hash(signup_form.password)
        payload = {
            "password": hashed_password,
            "created_on": str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            "updated_on": str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            "first_name": signup_form.first_name,
            "last_name": signup_form.last_name,
            "email": signup_form.email,
        }
        query = insert(models.User).values(**payload)
        await self.db.execute(query=query)
        new_user = await self.db.fetch_one(select(models.User).filter_by(email=payload.get("email")))
        return new_user

    async def create_user_auth0_if_not_exists(self, token: str) -> user_schemas.User:
        payload = jwt.decode(token=token, key=os.getenv("SECRET_KEY"), algorithms=os.getenv("ALGORITHM"))
        email = payload.get("user_email")
        user = await self.db.fetch_one(select(models.User).filter_by(email=email))
        if not user:
            user_details = {
                "password": token,
                "created_on": str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                "updated_on": str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                "first_name": token,
                "last_name": token,
                "email": email,
            }
            query = insert(models.User).values(**user_details)
            await self.db.execute(query=query)
            user = await self.db.fetch_one(select(models.User).filter_by(email=user_details.get("email")))
        return user

    @staticmethod
    async def update_user_details(user: user_schemas.User, user_upd: user_schemas.UserUpdate) -> user_schemas.User:
        updates = {}
        for key in user._mapping.keys():
            if key == "updated_on":
                updates["updated_on"] = str(datetime.datetime.now().strftime("%Y-%m-%d%H:%M:%S"))
            elif key not in user_upd.dict() or user_upd.dict()[key] is None:
                continue
            else:
                updates[key] = user_upd.dict()[key]
        return updates

    async def update_user(self, user_id: int, user_upd: user_schemas.UserUpdate) -> user_schemas.User:
        user = await self.user_exists(user_id=user_id)
        user_update_dict = await self.update_user_details(user=user, user_upd=user_upd)
        await self.db.execute(update(models.User).filter_by(id=user_id), values=user_update_dict)
        updated_user = await self.db.fetch_one(select(models.User).filter_by(id=user_id))
        return updated_user

    async def delete_user(self, user_id: int) -> status.HTTP_200_OK:
        await self.db.execute(delete(models.User).filter_by(id=user_id))
        return status.HTTP_200_OK
