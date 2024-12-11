from pydantic import BaseModel, ConfigDict
from typing import Literal
from enum import Enum

class FoodCategory(str, Enum):
    FRUITS = "fruits"
    VEGETABLES = "vegetables"
    PROTEINS = "proteins"
    CARBS = "carbs"
    DAIRY = "dairy"
    DRINKS = "drinks"
    SNACKS = "snacks"

class UnitType(str, Enum):
    UNIT = "unit"
    WEIGHT = "weight"
    VOLUME = "volume"
    SERVING = "serving"
    SPOON = "spoon"

class Food(BaseModel):
    name: str  # identifiant technique
    label: str  # label localisé
    category: FoodCategory
    unit_type: UnitType
    default_quantity: float

    class Config:
        from_attributes = True