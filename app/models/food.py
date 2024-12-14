from sqlalchemy import Column, BigInteger, String, Float, DateTime, Enum, func, and_
from sqlalchemy.orm import relationship
from app.database import Base
from enum import Enum
from sqlalchemy import Enum as SQLAlchemyEnum

class FoodCategory(str, Enum):
    fruits = "fruits"
    vegetables = "vegetables"
    proteins = "proteins"
    carbs = "carbs"
    dairy = "dairy"
    drinks = "drinks"
    snacks = "snacks"

class UnitType(str, Enum):
    unit = "unit"
    weight = "weight"
    volume = "volume"
    serving = "serving"
    spoon = "spoon"

class Food(Base):
    __tablename__ = "foods"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    category = Column(SQLAlchemyEnum(FoodCategory, name="foodcategory"))
    unit_type = Column(SQLAlchemyEnum(UnitType, name="unittype"), nullable=False)
    default_quantity = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relations
    meal_items = relationship("MealItem", back_populates="food")
    events = relationship("Event", secondary="meal_items", viewonly=True)