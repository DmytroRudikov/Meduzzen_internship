from pydantic import BaseModel


class SigninRequest(BaseModel):
    email: str
    password: str


class SignupRequest(SigninRequest):
    first_name: str
    last_name: str


class UserBasic(BaseModel):
    id: int
    first_name: str
    last_name: str
    status: str
    created_on: str
    updated_on: str

    class Config:
        orm_mode = True


class UserUpdate(UserBasic):
    password: str


class UserFull(UserUpdate):
    email: str


class User(UserBasic):
    email: str
