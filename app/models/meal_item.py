from sqlalchemy import Column, BigInteger, Float, ForeignKey, DateTime, func, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database import Base

class MealItem(Base):
    __tablename__ = "meal_items"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    event_id = Column(BigInteger, ForeignKey("events.id"), nullable=False)
    food_id = Column(BigInteger, ForeignKey("foods.id"), nullable=False)
    quantity = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relations
    event = relationship("Event", back_populates="meal_items")
    food = relationship("Food", back_populates="meal_items")

    # Contraintes
    __table_args__ = (
        UniqueConstraint('event_id', 'food_id', name='uq_event_food'),
    ) 