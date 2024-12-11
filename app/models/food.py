from sqlalchemy import Column, BigInteger, String, Float, DateTime, Enum, func
from sqlalchemy.orm import relationship
from app.database import Base
import enum
from datetime import datetime

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
    name = Column(String, nullable=False)
    category = Column(Enum(FoodCategory), nullable=False)
    unit_type = Column(Enum(UnitType), nullable=False)
    default_quantity = Column(Float, nullable=False)
    language = Column(String, nullable=False)
    localized_label = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

    # Relation directe avec meal_items
    meal_items = relationship("MealItem", back_populates="food")
    # Relation indirecte avec events via meal_items
    events = relationship("Event", secondary="meal_items", viewonly=True)