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
    company_relationship = relationship("Company", back_populates="owner_relationship", cascade="all, delete", passive_deletes=True)
    member_relationship = relationship("MemberRecord", back_populates="user_relationship", cascade="all, delete", passive_deletes=True)
    request_relationship = relationship("Request", back_populates="user_relationship", cascade="all, delete", passive_deletes=True)
    invite_relationship = relationship("Invite", back_populates="user_relationship", cascade="all, delete", passive_deletes=True)


class Company(Base):
    __tablename__ = "companies"

    company_id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String, nullable=False, unique=True)
    company_description = Column(String)
    company_owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    company_visible = Column(Boolean)
    created_on = Column(String, nullable=False)
    updated_on = Column(String, nullable=False)
    owner_relationship = relationship("User", back_populates="company_relationship")
    member_relationship = relationship("MemberRecord", back_populates="company_relationship", cascade="all, delete", passive_deletes=True)
    request_relationship = relationship("Request", back_populates="company_relationship", cascade="all, delete", passive_deletes=True)
    invite_relationship = relationship("Invite", back_populates="company_relationship", cascade="all, delete", passive_deletes=True)


class MemberRecord(Base):
    __tablename__ = "member_records"

    member_record_id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.company_id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    company_member_id = Column(Integer, nullable=False)
    role = Column(String)
    created_on = Column(String, nullable=False)
    updated_on = Column(String, nullable=False)
    user_relationship = relationship("User", back_populates="member_relationship")
    company_relationship = relationship("Company", back_populates="member_relationship")


class Request(Base):
    __tablename__ = "requests"

    request_id = Column(Integer, primary_key=True, index=True)
    from_user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    to_company_id = Column(Integer, ForeignKey("companies.company_id", ondelete="CASCADE"), nullable=False)
    request_message = Column(String, nullable=False)
    created_on = Column(String, nullable=False)
    updated_on = Column(String, nullable=False)
    status = Column(String)
    user_relationship = relationship("User", back_populates="request_relationship")
    company_relationship = relationship("Company", back_populates="request_relationship")


class Invite(Base):
    __tablename__ = "invites"

    invite_id = Column(Integer, primary_key=True, index=True)
    to_user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    from_company_id = Column(Integer, ForeignKey("companies.company_id", ondelete="CASCADE"), nullable=False)
    invite_message = Column(String, nullable=False)
    created_on = Column(String, nullable=False)
    updated_on = Column(String, nullable=False)
    status = Column(String)
    user_relationship = relationship("User", back_populates="invite_relationship")
    company_relationship = relationship("Company", back_populates="invite_relationship")
