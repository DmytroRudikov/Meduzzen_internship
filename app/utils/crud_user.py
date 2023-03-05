from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.schemas import schemas
from app.db import models
from passlib.context import CryptContext
import datetime
from fastapi import HTTPException, Response, status

context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def get_user(session: AsyncSession, user_id: int, response: Response):
    result = await session.execute(select(models.User).where(models.User.id == user_id))
    if result.scalars().first() is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return HTTPException(status_code=404, detail="User with this id does not exist")
    result = await session.execute(select(models.User).where(models.User.id == user_id))
    return result.scalar_one()


async def get_all_users(session: AsyncSession):
    result = await session.execute(select(models.User))
    return result.scalars().all()


async def create_user(session: AsyncSession, signup_form: schemas.SignupRequest, response: Response):
    user_exists = await session.execute(select(models.User).where(models.User.email == signup_form.email))
    if user_exists.scalars().first():
        response.status_code = status.HTTP_400_BAD_REQUEST
        return HTTPException(status_code=400, detail="User with this email already exists")
    hashed_password = context.hash(signup_form.password)
    created_on = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    updated_on = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    form_dict = signup_form.dict()
    form_dict["password"] = hashed_password
    form_dict.pop("password_check")
    new_user = models.User(**form_dict, created_on=created_on, updated_on=updated_on)
    session.add(new_user)
    await session.commit()
    return new_user


async def update_user(session: AsyncSession, user_id: int, user_upd: schemas.UserUpdate, response: Response):
    user = await session.execute(select(models.User).filter_by(id=user_id))
    if user.scalars().first() is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return HTTPException(status_code=404, detail="User with this id does not exist")
    user = await session.execute(select(models.User).filter_by(id=user_id))
    for key in user.scalar_one().__table__.columns.keys():
        if key == "updated_on":
            user = await session.execute(select(models.User).filter_by(id=user_id))
            setattr(user.scalar_one(), key, str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        elif key not in user_upd.dict() or user_upd.dict()[key] is None:
            continue
        else:
            user = await session.execute(select(models.User).filter_by(id=user_id))
            setattr(user.scalar_one(), key, user_upd.dict()[key])
    user = await session.execute(select(models.User).filter_by(id=user_id))
    updated_user = user.scalar_one()
    await session.commit()
    return updated_user


async def delete_user(session: AsyncSession, user_id: int):
    to_delete = await session.execute(select(models.User).where(models.User.id == user_id))
    await session.delete(to_delete.scalar_one())
    await session.commit()
    return
