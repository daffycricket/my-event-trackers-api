from typing import List, Optional, Dict, Any
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from uuid import UUID

# Schémas pour MealItem
class MealItemBase(BaseModel):
    name: str
    quantity: float
    
    model_config = ConfigDict(from_attributes=True)

class MealItemCreate(MealItemBase):
    pass

class MealItem(MealItemBase):
    id: UUID
    event_id: UUID
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# Schémas pour Event
class EventBase(BaseModel):
    type: str
    date: datetime
    data: Dict[str, Any]
    notes: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)

class EventCreate(EventBase):
    pass

class EventUpdate(EventBase):
    type: Optional[str] = None
    date: Optional[datetime] = None
    data: Optional[Dict[str, Any]] = None
    notes: Optional[str] = None

class Event(EventBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    meal_items: List[MealItem] = []
    
    model_config = ConfigDict(from_attributes=True) 