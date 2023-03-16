import sys
import os
sys.path.append(os.getcwd())

from app.schemas import token_schemas, user_schemas
from fastapi import APIRouter, Depends
from app.utils import authorisation
from app.utils.crud_user import UserCrud
from app.core.db_config import get_sql_db
from databases import Database

router = APIRouter()


@router.post("/auth/login", response_model=token_schemas.Token)
async def signin_and_get_token(login_form: user_schemas.SigninRequest, db: Database = Depends(get_sql_db)) -> token_schemas.Token:
    crud_user = UserCrud(db=db)
    return await authorisation.get_token_at_signin(login_form=login_form, crud_user=crud_user)
