from sqlalchemy import Column, BigInteger, String, Float, DateTime, Enum, func, and_
from sqlalchemy.orm import relationship
from app.database import Base
import enum

class FoodCategory(str, enum.Enum):
    FRUITS = "fruits"
    VEGETABLES = "vegetables"
    PROTEINS = "proteins"
    CARBS = "carbs"
    DAIRY = "dairy"
    DRINKS = "drinks"
    SNACKS = "snacks"

class UnitType(str, enum.Enum):
    UNIT = "unit"
    WEIGHT = "weight"
    VOLUME = "volume"
    SERVING = "serving"
    SPOON = "spoon"

class Food(Base):
    __tablename__ = "foods"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    category = Column(Enum(FoodCategory), nullable=False)
    unit_type = Column(Enum(UnitType), nullable=False)
    default_quantity = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relations
    meal_items = relationship("MealItem", back_populates="food")
    events = relationship("Event", secondary="meal_items", viewonly=True)