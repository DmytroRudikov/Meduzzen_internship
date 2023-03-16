from databases import Database
from app.schemas import user_schemas
from fastapi import APIRouter, Depends
from app.utils.authorisation import get_current_user
from typing import List
from app.utils.crud_user import UserCrud
from app.core.db_config import get_sql_db

router = APIRouter()


@router.get("/user", response_model=user_schemas.User)
async def get_user(user_id: int, db: Database = Depends(get_sql_db)) -> user_schemas.User:
    crud_user = UserCrud(db=db)
    return await crud_user.get_user(user_id=user_id)


@router.get("/auth/me", response_model=user_schemas.User)
async def return_current_user(db: Database = Depends(get_sql_db)) -> user_schemas.User:
    crud_user = UserCrud(db=db)
    return await get_current_user(crud_user=crud_user)


@router.get("/users", response_model=List[user_schemas.User])
async def get_all_users(db: Database = Depends(get_sql_db)) -> List[user_schemas.User]:
    crud_user = UserCrud(db=db)
    return await crud_user.get_all_users()


@router.post("/user", response_model=user_schemas.User)
async def create_user(signup_form: user_schemas.SignupRequest, db: Database = Depends(get_sql_db)) -> user_schemas.User:
    crud_user = UserCrud(db=db)
    return await crud_user.create_user(signup_form=signup_form)


@router.put("/user", response_model=user_schemas.User)
async def update_user(user_upd: user_schemas.UserUpdate, user_id: int, db: Database = Depends(get_sql_db)) -> user_schemas.User:
    crud_user = UserCrud(db=db)
    return await crud_user.update_user(user_id=user_id, user_upd=user_upd)


@router.delete("/user", status_code=200)
async def delete_user(user_id: int, db: Database = Depends(get_sql_db)):
    crud_user = UserCrud(db=db)
    return await crud_user.delete_user(user_id=user_id)
