from sqlalchemy import Column, String, Float, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class MealItem(BaseModel):
    __tablename__ = "meal_items"

    event_id = Column(UUID, ForeignKey('events.id', ondelete='CASCADE'))
    name = Column(String, nullable=False)
    quantity = Column(Float, nullable=False)

    event = relationship("Event", back_populates="meal_items")