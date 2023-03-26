from pydantic import BaseModel


class CreateRequest(BaseModel):
    to_company_id: int
    request_message: str


class Request(CreateRequest):
    from_user_id: int
    request_id: int
    created_on: str
    updated_on: str
    status: str | None = None
