from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from schemas import token_schemas, user_schemas
from utils.crud_user import context, UserCrud
import datetime
import os
from dotenv import load_dotenv

load_dotenv()


oauth_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
credentials_exception = HTTPException(status_code=401,
                                      detail="Incorrect username or password",
                                      headers={"WWW-Authenticate": "Bearer"})

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))


def verify_password(plain_password, hashed_password):
    return context.verify(plain_password, hashed_password)


async def authenticate_user(email: str, plain_password: str, crud_user: UserCrud) -> user_schemas.User:
    user = await crud_user.user_exists(email=email)
    if not verify_password(plain_password=plain_password, hashed_password=user_schemas.User.password):
        raise credentials_exception
    return user


def create_token(data: dict, expires_delta: datetime.timedelta):
    to_encode = data.copy()
    to_encode["exp"] = datetime.datetime.utcnow() + expires_delta
    encode_jwt = jwt.encode(claims=to_encode, key=SECRET_KEY, algorithm=ALGORITHM)
    return encode_jwt


async def get_token_at_signin(login_form: user_schemas.SigninRequest, crud_user: UserCrud) -> token_schemas.Token:
    user = await authenticate_user(email=login_form.email, plain_password=login_form.password, crud_user=crud_user)
    expires_delta = datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    data = {"user_email": user.email}
    access_token = create_token(data=data, expires_delta=expires_delta)
    return {"access_token": access_token, "token_type": "bearer"}


async def get_current_user(crud_user: UserCrud, token: str = Depends(oauth_scheme)) -> user_schemas.User:
    try:
        payload = jwt.decode(token=token, key=SECRET_KEY, algorithms=ALGORITHM)
        user_email = payload.get("user_email")
        if user_email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    else:
        user = await crud_user.user_exists(email=user_email)
        return user
