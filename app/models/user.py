from typing import List
from sqlalchemy import Column, String, Boolean
from sqlalchemy.dialects.postgresql import UUID
import uuid
from fastapi_users.db import SQLAlchemyBaseUserTable

from app.database import Base

class User(SQLAlchemyBaseUserTable[uuid.UUID], Base):
    __tablename__ = "user"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email: str = Column(String(length=320), unique=True, index=True, nullable=False)
    hashed_password: str = Column(String(length=1024), nullable=False)
    is_active: bool = Column(Boolean, default=True, nullable=False)
    is_superuser: bool = Column(Boolean, default=False, nullable=False)
    is_verified: bool = Column(Boolean, default=True, nullable=False)  # On met true par défaut puisqu'on ne vérifie pas les emails 