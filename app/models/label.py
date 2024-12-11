from sqlalchemy import Column, BigInteger, String, ForeignKey, DateTime, func, UniqueConstraint
import sqlalchemy
from sqlalchemy.orm import relationship
from app.database import Base

class Label(Base):
    __tablename__ = "labels"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    entity_type = Column(String, nullable=False)  # 'food', 'category', etc.
    entity_id = Column(BigInteger, nullable=False)
    language = Column(String, nullable=False)
    value = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Contrainte unique pour éviter les doublons
    __table_args__ = (
        UniqueConstraint('entity_type', 'entity_id', 'language', name='uq_label'),
    ) 