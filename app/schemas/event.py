from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
from app.models.event import EventType
from app.schemas.meal_item import MealItem

class MealItemBase(BaseModel):
    food_id: int
    quantity: float

    class Config:
        from_attributes = True

class EventBase(BaseModel):
    type: EventType
    date: datetime
    notes: Optional[str] = None

class EventCreate(BaseModel):
    type: str
    date: datetime
    notes: Optional[str] = None
    meal_items: Optional[List[MealItem]] = None

class EventUpdate(BaseModel):
    notes: Optional[str] = None
    meal_items: Optional[List[MealItem]] = None

class Event(EventBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    meal_items: Optional[List[MealItem]] = None

    class Config:
        from_attributes = True
        populate_by_name = True 