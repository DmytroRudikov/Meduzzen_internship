from pydantic import BaseModel, validator
from fastapi import HTTPException


class CompanyUpdate(BaseModel):
    company_name: str | None = None
    company_description: str | None = None
    company_visible: bool | None = None


class CreateCompany(BaseModel):
    company_name: str
    company_description: str | None = None
    company_visible: bool | None = None

    @validator("company_name")
    def name_not_empty(cls, company_name):
        if company_name == "" or company_name is None:
            raise HTTPException(status_code=422, detail="The company name must not be empty")
        return company_name


class Company(CreateCompany):
    company_id: int
    created_on: str
    updated_on: str
    company_owner_id: int

    class Config:
        orm_mode = True
