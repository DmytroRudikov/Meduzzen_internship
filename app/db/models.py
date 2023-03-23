from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    status = Column(String)
    password = Column(String, nullable=False)
    created_on = Column(String, nullable=False)
    updated_on = Column(String, nullable=False)
    company_relationship = relationship("Company", back_populates="owner_relationship")


class Company(Base):
    __tablename__ = "companies"

    company_id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String, nullable=False, unique=True)
    company_description = Column(String)
    owner_relationship = relationship("User", back_populates="company_relationship")
    company_owner_id = Column(Integer, ForeignKey("users.id"))
    company_visible = Column(Boolean)
    created_on = Column(String, nullable=False)
    updated_on = Column(String, nullable=False)
