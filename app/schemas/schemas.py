from pydantic import BaseModel


class User(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    password: str
    created_on: str
    updated_on: str

    class Config:
        orm_mode = True


class SigninRequest(User):
    pass


class SignupRequest(User):
    pass


class UserUpdate(User):
    pass


class UsersList(User):
    User: list[User]
