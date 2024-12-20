from typing import List
from sqlalchemy import BigInteger, String, Boolean, Column, DateTime, func
from sqlalchemy.orm import relationship
from app.database import Base
from fastapi_users.db import SQLAlchemyBaseUserTable

class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    email = Column(String(length=320), unique=True, index=True, nullable=False)
    hashed_password = Column(String(length=1024), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relations
    events = relationship("Event", back_populates="user", cascade="all, delete-orphan")