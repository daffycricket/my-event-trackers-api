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
    id: str  # On utilisera le champ 'name' de la BDD
    name: str  # On utilisera le champ 'localized_label' de la BDD
    category: FoodCategory
    unit_type: UnitType
    default_quantity: int

    model_config = ConfigDict(from_attributes=True)