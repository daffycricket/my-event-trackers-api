from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional, Dict
from app.models.event import EventType
from app.schemas.meal_item import MealItem
from enum import Enum
from pydantic import ConfigDict

class WorkoutType(str, Enum):
    RUNNING = "running"
    CYCLING = "cycling"
    FITNESS = "fitness"
    STRENGTH = "strength"
    OTHER = "other"

class MealType(str, Enum):
    BREAKFAST = "breakfast"
    LUNCH = "lunch"
    DINNER = "dinner"
    SNACK = "snack"

class WorkoutData(BaseModel):
    duration: int  # en minutes
    calories_burned: int
    workout_type: WorkoutType

class MealData(BaseModel):
    meal_type: MealType

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
    data: Optional[Dict] = None

class EventUpdate(BaseModel):
    notes: Optional[str] = None
    meal_items: Optional[List[MealItem]] = None
    data: Optional[Dict] = None

class Event(BaseModel):
    id: int
    type: EventType
    date: datetime
    notes: Optional[str] = None
    data: Optional[Dict] = None
    user_id: int
    created_at: datetime
    updated_at: datetime
    meal_items: Optional[List[MealItem]] = None

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        exclude_none=True
    )