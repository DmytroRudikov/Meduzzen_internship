from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from databases import Database
from jose import jwt, JWTError
from app.schemas import token_schemas, user_schemas
from app.services.crud_user import context, UserCrud
from app.core.db_config import get_sql_db
import datetime
import os
from dotenv import load_dotenv

load_dotenv()


class Auth:

    oauth_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

    def __init__(self):
        self.credentials_exception = HTTPException(status_code=401,
                                                   detail="Incorrect username or password",
                                                   headers={"WWW-Authenticate": "Bearer"})
        self.SECRET_KEY = os.getenv("SECRET_KEY")
        self.ALGORITHM = os.getenv("ALGORITHM")
        self.ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

    @staticmethod
    def verify_password(plain_password, hashed_password):
        return context.verify(plain_password, hashed_password)

    async def authenticate_user(self, email: str, plain_password: str) -> user_schemas.User:
        crud_user = UserCrud(db=get_sql_db())
        user = await crud_user.user_exists_for_auth(email=email)
        if not self.verify_password(plain_password=plain_password, hashed_password=user.password):
            raise self.credentials_exception
        return user

    def create_token(self, data: dict, expires_delta: datetime.timedelta):
        to_encode = data.copy()
        expire = datetime.datetime.utcnow() + expires_delta
        to_encode.update({"exp": expire})
        encode_jwt = jwt.encode(claims=to_encode, key=self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encode_jwt

    async def get_token_at_signin(self, login_form: user_schemas.SigninRequest) -> token_schemas.Token:
        user = await self.authenticate_user(email=login_form.email, plain_password=login_form.password)
        expires_delta = datetime.timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)
        data = {"user_email": user.email}
        access_token = self.create_token(data=data, expires_delta=expires_delta)
        return {"access_token": access_token, "token_type": "Bearer"}

    async def get_current_user(self, token: str = Depends(oauth_scheme)) -> user_schemas.User:
        crud_user = UserCrud(db=get_sql_db())
        try:
            payload = jwt.decode(token=token, key=self.SECRET_KEY, algorithms=self.ALGORITHM)
            user_email = payload.get("user_email")
            if user_email is None:
                raise self.credentials_exception
        except JWTError:
            raise self.credentials_exception
        else:
            user = crud_user.user_exists_for_auth(email=user_email)
            return user
