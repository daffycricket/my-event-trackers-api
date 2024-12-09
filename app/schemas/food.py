from pydantic import BaseModel
from enum import Enum

class UnitType(str, Enum):
    UNIT = "unit"        # unité (ex: 1 pomme)
    WEIGHT = "weight"    # grammes
    VOLUME = "volume"    # centilitres
    SERVING = "serving"  # portion
    SPOON = "spoon"     # cuillère

class FoodCategory(str, Enum):
    FRUITS = "fruits"
    VEGETABLES = "vegetables"
    PROTEINS = "proteins"
    CARBS = "carbs"
    DAIRY = "dairy"
    DRINKS = "drinks"
    SNACKS = "snacks"

class FoodItem(BaseModel):
    id: str
    name: str
    category: FoodCategory
    unit_type: UnitType
    default_quantity: float = 1.0 