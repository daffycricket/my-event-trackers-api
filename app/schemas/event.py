from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
from app.models.event import EventType

class MealItemBase(BaseModel):
    food_id: int
    quantity: float

    class Config:
        from_attributes = True

class EventBase(BaseModel):
    type: EventType
    date: datetime
    notes: Optional[str] = None

class EventCreate(EventBase):
    meal_items: Optional[List[MealItemBase]] = None

class EventUpdate(EventBase):
    type: Optional[EventType] = None
    date: Optional[datetime] = None
    meal_items: Optional[List[MealItemBase]] = None

class Event(EventBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    meal_items: List[MealItemBase] = []

    class Config:
        from_attributes = True
        populate_by_name = True 