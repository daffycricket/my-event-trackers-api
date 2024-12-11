from sqlalchemy import Column, BigInteger, String, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from typing import List

from .base import Base
from .meal_item import MealItem

class Event(Base):
    __tablename__ = "events"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    type = Column(String, nullable=False)
    date = Column(DateTime, nullable=False)
    notes = Column(String, nullable=True)
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relation avec meal_items
    meal_items = relationship("MealItem", lazy="selectin")