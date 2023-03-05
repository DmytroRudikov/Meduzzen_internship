from app.core.db_config import Base
from sqlalchemy import Column, Integer, String


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
