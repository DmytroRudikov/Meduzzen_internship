from pydantic import BaseModel, validator, EmailStr
from email_validator import validate_email, EmailNotValidError
from fastapi import HTTPException


class SigninRequest(BaseModel):
    email: EmailStr
    password: str

    @validator("password")
    def password_not_empty(cls, password):
        if password == "" or password is None:
            return HTTPException(status_code=422, detail="The password must not be empty")
        return password


class SignupRequest(SigninRequest):
    first_name: str
    last_name: str
    password_check: str

    @validator("password_check")
    def password_match(cls, password_check, values):
        print(password_check, values)
        if "password" in values and password_check != values["password"]:
            raise ValueError("Passwords do not match")
        return password_check


class User(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    password: str
    status: str | None = None
    created_on: str
    updated_on: str

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    status: str | None = None
    password: str | None = None
