from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from schemas import token_schemas, user_schemas
from core.classes_config import crud_user
from utils.crud_user import context
import datetime
import os


oauth_scheme = OAuth2PasswordBearer(tokenUrl="signin")
credentials_exception = HTTPException(status_code=401,
                                      detail="Credentials provided are not correct. Validation failed.",
                                      headers={"WWW-Authenticate": "Bearer"})

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def verify_password(plain_password, hashed_password):
    return context.verify(plain_password, hashed_password)


async def authenticate_user(email: str, plain_password: str):
    user = await crud_user.user_exists(email=email)
    if not verify_password(plain_password=plain_password, hashed_password=user_schemas.User.password):
        raise credentials_exception
    return user


def create_token(data: dict, expires_delta: datetime.timedelta):
    to_encode = data.copy()
    to_encode["exp"] = datetime.datetime.utcnow() + expires_delta
    encode_jwt = jwt.encode(claims=to_encode, key=SECRET_KEY, algorithm=ALGORITHM)
    return encode_jwt


async def get_token_at_signin(login_form: user_schemas.SigninRequest):
    user = await authenticate_user(email=login_form.email, plain_password=login_form.password)
    expires_delta = datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    data = {"sub": user.email}
    access_token = create_token(data=data, expires_delta=expires_delta)
    return {"access_token": access_token, "token_type": "bearer"}


async def get_current_user(token: str = Depends(oauth_scheme)) -> user_schemas.User:
    try:
        payload = jwt.decode(token=token, key=SECRET_KEY, algorithms=ALGORITHM)
        user_email = payload.get("sub")
        if user_email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    else:
        user = await self.user_exists(email=user_email)
        return user
