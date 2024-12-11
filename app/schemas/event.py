from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, List
from .meal_item import MealItem, MealItemData

class EventBase(BaseModel):
    type: str
    date: datetime
    notes: Optional[str] = None

class EventCreate(EventBase):
    meal_items: Optional[List[MealItemData]] = None

class EventUpdate(BaseModel):
    type: Optional[str] = None
    date: Optional[datetime] = None
    notes: Optional[str] = None
    meal_items: Optional[List[MealItemData]] = None

# Pour la réponse, on cache les champs techniques
class Event(EventBase):
    id: int
    meal_items: List[MealItem] = []

    model_config = ConfigDict(
        from_attributes=True,
        # On exclut les champs techniques de la sérialisation
        exclude={"created_at", "updated_at"}
    ) 