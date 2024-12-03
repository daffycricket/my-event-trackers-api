from datetime import datetime
from typing import Optional, List, Union
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict
from enum import Enum

class EventType(str, Enum):
    MEAL = "MEAL"
    WORKOUT = "WORKOUT"

class MealType(str, Enum):
    breakfast = "breakfast"
    lunch = "lunch"
    dinner = "dinner"
    snack = "snack"

class WorkoutType(str, Enum):
    cardio = "cardio"
    strength = "strength"
    flexibility = "flexibility"
    sport = "sport"

class FoodItem(BaseModel):
    id: str
    date: datetime
    notes: Optional[str] = None

    model_config = ConfigDict(json_encoders={datetime: lambda v: v.isoformat()})

class MealData(BaseModel):
    foods: List[FoodItem]
    type: MealType

    model_config = ConfigDict(json_encoders={datetime: lambda v: v.isoformat()})

class WorkoutData(BaseModel):
    duration: int
    type: WorkoutType
    calories_burned: Optional[int] = None

class EventBase(BaseModel):
    type: EventType
    date: datetime
    notes: Optional[str] = None
    data: Union[MealData, WorkoutData]

    model_config = ConfigDict(json_encoders={datetime: lambda v: v.isoformat()})

class EventCreate(EventBase):
    pass

class EventUpdate(EventBase):
    pass

class Event(EventBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True) 