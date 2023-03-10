from app.schemas import schemas
from fastapi import Depends, Response, APIRouter
from app.utils.crud_user import UserCrud
from typing import List
from app.core.db_config import get_sql_db

router = APIRouter()
crud_user = UserCrud(get_sql_db())


@router.get("/user", response_model=schemas.User)
async def get_user(user_id: int) -> schemas.User:
    return await crud_user.get_user(user_id=user_id)


@router.get("/users", response_model=List[schemas.User])
async def get_all_users() -> List[schemas.User]:
    return await crud_user.get_all_users()


@router.post("/user", response_model=schemas.User)
async def create_user(signup_form: schemas.SignupRequest) -> schemas.User:
    return await crud_user.create_user(signup_form=signup_form)


@router.put("/user", response_model=schemas.User)
async def update_user(user_upd: schemas.UserUpdate, user_id: int) -> schemas.User:
    return await crud_user.update_user(user_id=user_id, user_upd=user_upd)


@router.delete("/user", status_code=200)
async def delete_user(user_id: int):
    return await crud_user.delete_user(user_id=user_id)
