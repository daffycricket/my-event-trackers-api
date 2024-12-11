from pydantic import BaseModel

class MealItemBase(BaseModel):
    name: str
    quantity: float

class MealItemCreate(MealItemBase):
    pass

class MealItemInDB(MealItemBase):
    id: int
    event_id: int
    food_id: int

class MealItem(MealItemBase):
    """Utilisé pour les réponses API"""
    pass