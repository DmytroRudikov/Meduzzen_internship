import sys
import os
sys.path.append(os.getcwd())
from app.schemas import schemas
from app.db import models
from databases import Database
from passlib.context import CryptContext
import datetime
from fastapi import HTTPException, Response, status
from sqlalchemy import insert, select, delete, update

context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def get_user(db: Database, user_id: int, response: Response):
    result = await db.fetch_one(select(models.User).filter_by(id=user_id))
    if result is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        raise HTTPException(status_code=404, detail="User with this id does not exist")
    return result


async def get_all_users(db: Database):
    result = await db.fetch_all("SELECT * FROM users")
    return result


async def create_user(db: Database, signup_form: schemas.SignupRequest, response: Response):
    user_exists = await db.fetch_one(select(models.User).filter_by(email=signup_form.email))
    if user_exists:
        response.status_code = status.HTTP_400_BAD_REQUEST
        raise HTTPException(status_code=400, detail="User with this email already exists")
    hashed_password = context.hash(signup_form.password)
    created_on = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    updated_on = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    form_dict = signup_form.dict()
    form_dict["password"] = hashed_password
    form_dict["created_on"] = created_on
    form_dict["updated_on"] = updated_on
    form_dict.pop("password_check")
    query = insert(models.User).values(**form_dict)
    await db.execute(query=query)
    new_user = await db.fetch_one(select(models.User).filter_by(email=form_dict["email"]))
    return new_user


async def update_user(db: Database, user_id: int, user_upd: schemas.UserUpdate, response: Response):
    user = await db.fetch_one(select(models.User).filter_by(id=user_id))
    if user is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        raise HTTPException(status_code=404, detail="User with this id does not exist")
    for key in user._mapping.keys():
        if key == "updated_on":
            await db.execute(update(models.User).filter_by(id=user_id).values(updated_on=str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))))
        elif key not in user_upd.dict() or user_upd.dict()[key] is None:
            continue
        else:
            await db.execute(update(models.User).filter_by(id=user_id), values={key: user_upd.dict()[key]})
    updated_user = await db.fetch_one(select(models.User).filter_by(id=user_id))
    return updated_user


async def delete_user(db: Database, user_id: int):
    await db.execute(delete(models.User).filter_by(id=user_id))
    return
