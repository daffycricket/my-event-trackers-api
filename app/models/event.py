from sqlalchemy import Column, String, DateTime, JSON, Enum, event
import enum
from uuid import uuid4
from datetime import datetime
import json

from .base import BaseModel

class EventType(str, enum.Enum):
    MEAL = "MEAL"
    WORKOUT = "WORKOUT"

class MealType(str, enum.Enum):
    breakfast = "breakfast"
    lunch = "lunch"
    dinner = "dinner"
    snack = "snack"

class WorkoutType(str, enum.Enum):
    cardio = "cardio"
    strength = "strength"
    flexibility = "flexibility"
    sport = "sport"

def json_serializer(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    if isinstance(obj, enum.Enum):
        return obj.value
    raise TypeError(f'Type {type(obj)} not serializable')

class Event(BaseModel):
    __tablename__ = "events"

    type = Column(Enum(EventType), nullable=False)
    date = Column(DateTime, nullable=False)
    data = Column(JSON, nullable=False)
    notes = Column(String, nullable=True)

@event.listens_for(Event, 'before_insert')
@event.listens_for(Event, 'before_update')
def serialize_json_data(mapper, connection, target):
    if target.data:
        target.data = json.loads(json.dumps(target.data, default=json_serializer))