from app.schemas import user_schemas
from fastapi import APIRouter, Depends
from app.core.classes_config import crud_user
from app.utils.authorisation import get_current_user
from typing import List
from app.core.db_config import get_sql_db

router = APIRouter()


@router.get("/user", response_model=user_schemas.User)
async def get_user(user_id: int) -> user_schemas.User:
    return await crud_user.get_user(user_id=user_id)


@router.get("/user/me", response_model=user_schemas.User)
async def get_current_user(current_user: user_schemas.User = Depends(get_current_user)) -> user_schemas.User:
    return await current_user


@router.get("/users", response_model=List[user_schemas.User])
async def get_all_users() -> List[user_schemas.User]:
    return await crud_user.get_all_users()


@router.post("/user", response_model=user_schemas.User)
async def create_user(signup_form: user_schemas.SignupRequest) -> user_schemas.User:
    return await crud_user.create_user(signup_form=signup_form)


@router.put("/user", response_model=user_schemas.User)
async def update_user(user_upd: user_schemas.UserUpdate, user_id: int) -> user_schemas.User:
    return await crud_user.update_user(user_id=user_id, user_upd=user_upd)


@router.delete("/user", status_code=200)
async def delete_user(user_id: int):
    return await crud_user.delete_user(user_id=user_id)
