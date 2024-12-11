from sqlalchemy import Column, BigInteger, Float, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database import Base

class MealItem(Base):
    __tablename__ = "meal_items"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    quantity = Column(Float, nullable=False)
    event_id = Column(BigInteger, ForeignKey("events.id"), nullable=False)
    food_id = Column(BigInteger, ForeignKey("foods.id"), nullable=False)

    # Relations bidirectionnelles
    event = relationship("Event", back_populates="meal_items")
    food = relationship("Food", back_populates="meal_items")

    # Contrainte d'unicité composite
    __table_args__ = (
        UniqueConstraint('event_id', 'food_id', name='uq_event_food'),
    ) 