import sys
import os
sys.path.append(os.getcwd())

from databases import Database
from app.schemas import user_schemas
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.services.crud_user import UserCrud
from app.core.db_config import get_sql_db
from app.core.authorisation import Auth

router = APIRouter()
auth = Auth()


@router.get("/user", response_model=user_schemas.User)
async def get_user(user_id: int, db: Database = Depends(get_sql_db), user: user_schemas.User = Depends(auth.get_current_user)) -> user_schemas.User:
    crud_user = UserCrud(db=db)
    return await crud_user.get_user(user_id=user_id)


@router.get("/users", response_model=List[user_schemas.User])
async def get_all_users(db: Database = Depends(get_sql_db), user: user_schemas.User = Depends(auth.get_current_user)) -> List[user_schemas.User]:
    crud_user = UserCrud(db=db)
    return await crud_user.get_all_users()


@router.post("/user", response_model=user_schemas.User)
async def create_user(signup_form: user_schemas.SignupRequest, db: Database = Depends(get_sql_db)) -> user_schemas.User:
    crud_user = UserCrud(db=db)
    return await crud_user.create_user(signup_form=signup_form)


@router.put("/user", response_model=user_schemas.User)
async def update_user(user_upd: user_schemas.UserUpdate, user_id: int, db: Database = Depends(get_sql_db), user: user_schemas.User = Depends(auth.get_current_user)) -> user_schemas.User:
    crud_user = UserCrud(db=db)
    user_in_db = await user
    if user_in_db.id != user_id:
        raise HTTPException(status_code=403, detail="It's not your account")
    return await crud_user.update_user(user_id=user_id, user_upd=user_upd)


@router.delete("/user", status_code=200)
async def delete_user(user_id: int, db: Database = Depends(get_sql_db), user: user_schemas.User = Depends(auth.get_current_user)):
    crud_user = UserCrud(db=db)
    user_in_db = await user
    if user_in_db.id != user_id:
        raise HTTPException(status_code=403, detail="It's not your account")
    return await crud_user.delete_user(user_id=user_id)
