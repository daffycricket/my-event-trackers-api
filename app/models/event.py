from sqlalchemy import Column, BigInteger, String, DateTime, ForeignKey, Enum, func, JSON
from sqlalchemy.orm import relationship
from app.database import Base
import enum

class EventType(str, enum.Enum):
    MEAL = "MEAL"
    WORKOUT = "WORKOUT"

class Event(Base):
    __tablename__ = "events"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    type = Column(Enum(EventType), nullable=False)
    date = Column(DateTime(timezone=True), nullable=False)
    notes = Column(String, nullable=True)
    data = Column(JSON, nullable=False, server_default='{}')
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relations
    user = relationship("User", back_populates="events")
    meal_items = relationship("MealItem", back_populates="event", cascade="all, delete-orphan")