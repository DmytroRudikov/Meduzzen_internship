from pydantic import BaseModel


class Admin(BaseModel):
    company_member_id: int


class Member(Admin):
    member_record_id: int
    company_id: int
    user_id: int
    role: str | None = None
    created_on: str
    updated_on: str
