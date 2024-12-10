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
    data: Optional[Dict] = None
    notes: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)

class EventCreate(EventBase):
    pass

class EventUpdate(EventBase):
    pass

class Event(EventBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    user_id: UUID
    
    model_config = ConfigDict(from_attributes=True) 