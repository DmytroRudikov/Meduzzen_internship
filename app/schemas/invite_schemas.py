from pydantic import BaseModel


class CreateInvite(BaseModel):
    to_user_id: int
    from_company_id: int
    invite_message: str


class Invite(CreateInvite):
    invite_id: int
    created_on: str
    updated_on: str
    status: str | None = None
