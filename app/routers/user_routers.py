from app.routers.general_routers import connect_to_db
from app.schemas import schemas
from fastapi import Depends, Response, APIRouter
from app.utils import crud_user
from typing import List
from databases import Database

router = APIRouter()


@router.get("/user", response_model=schemas.User)
async def get_user(user_id: int, response: Response, db: Database = Depends(connect_to_db)):
    return await crud_user.get_user(db=db, user_id=user_id, response=response)


@router.get("/users", response_model=List[schemas.User])
async def get_all_users(db: Database = Depends(connect_to_db)):
    return await crud_user.get_all_users(db)


@router.post("/user", response_model=schemas.User)
async def create_user(signup_form: schemas.SignupRequest, response: Response, db: Database = Depends(connect_to_db)):
    return await crud_user.create_user(db=db, signup_form=signup_form, response=response)


@router.put("/user", response_model=schemas.User)
async def update_user(user_upd: schemas.UserUpdate, user_id: int, response: Response, db: Database = Depends(connect_to_db)):
    return await crud_user.update_user(db=db, user_id=user_id, user_upd=user_upd, response=response)


@router.delete("/user")
async def delete_user(user_id: int, db: Database = Depends(connect_to_db)):
    return await crud_user.delete_user(db, user_id)
