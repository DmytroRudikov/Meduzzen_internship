from pydantic import BaseModel


class Member(BaseModel):
    member_record_id: int
    company_id: int
    user_id: int
    company_member_id: int
    role: str | None = None
    created_on: str
    updated_on: str
