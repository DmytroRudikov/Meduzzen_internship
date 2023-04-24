from app.schemas import token_schemas, user_schemas
from fastapi import APIRouter, Depends
from app.core.authorisation import Auth, get_current_user

router = APIRouter()
auth = Auth()


@router.post("/auth/login", response_model=token_schemas.Token)
async def signin_and_get_token(login_form: user_schemas.SigninRequest) -> token_schemas.Token:
    return await auth.signin(login_form=login_form)


@router.get("/auth/me", response_model=user_schemas.UserNoPassword)
async def get_current_user(user: user_schemas.User = Depends(get_current_user)) -> user_schemas.UserNoPassword:
    return user
