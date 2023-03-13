from app.schemas import token_schemas, user_schemas
from fastapi import APIRouter
from app.utils import authorisation

router = APIRouter()


@router.post("/signin", response_model=token_schemas.Token)
async def signin_and_get_token(login_form: user_schemas.SigninRequest) -> token_schemas.Token:
    return await authorisation.get_token_at_signin(login_form=login_form)
