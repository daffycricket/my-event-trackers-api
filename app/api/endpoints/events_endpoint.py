from typing import List, Optional
from uuid import UUID
import uuid
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.schemas.event import Event, EventCreate, EventUpdate
from app.models import Event as EventModel, Food
from app.models.user import User
from app.auth.config import fastapi_users

router = APIRouter(
    prefix="/api/events",
    tags=["events"]
)

current_active_user = fastapi_users.current_user(active=True)

@router.get("", response_model=List[Event])
async def read_events(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(current_active_user)
):
    query = select(EventModel).where(EventModel.user_id == user.id).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()

@router.post("", response_model=Event)
async def create_event(
    event: EventCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(current_active_user)
):
    now = datetime.utcnow()
    # Convertir la date en naive datetime
    event_date = event.date.replace(tzinfo=None)
    
    db_event = EventModel(
        id=uuid.uuid4(),
        type=event.type,
        date=event_date,  # Date sans timezone
        data=event.data,
        notes=event.notes,
        user_id=user.id,
        created_at=now,
        updated_at=now
    )
    db.add(db_event)
    await db.commit()
    await db.refresh(db_event)
    return db_event

@router.get("/version")
def get_version():
    return {
        "version": "1.0.0",
        "name": "Event Tracker API",
        "description": "API de gestion d'événements pour le suivi des repas et des entraînements",
        "environment": "production"
    }

@router.get("/test")
def test_reload():
    return {"message": "Test reload working!"}

@router.get("/search", response_model=List[Event])
def search_events(q: str, db: Session = Depends(get_db)):
    events = db.query(EventModel).filter(
        EventModel.notes.ilike(f"%{q}%")
    ).all()
    return events

@router.get("/{event_id}", response_model=Event)
def read_event(event_id: UUID, db: Session = Depends(get_db)):
    if (event := db.query(EventModel).filter(EventModel.id == event_id).first()) is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

@router.put("/{event_id}", response_model=Event)
def update_event(event_id: UUID, event: EventUpdate, db: Session = Depends(get_db)):
    if (db_event := db.query(EventModel).filter(EventModel.id == event_id).first()) is None:
        raise HTTPException(status_code=404, detail="Event not found")
    
    update_data = event.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_event, key, value)
    
    db.commit()
    db.refresh(db_event)
    return db_event

@router.delete("/{event_id}")
def delete_event(event_id: UUID, db: Session = Depends(get_db)):
    if (event := db.query(EventModel).filter(EventModel.id == event_id).first()) is None:
        raise HTTPException(status_code=404, detail="Event not found")
    
    db.delete(event)
    db.commit()
    return {"status": "success", "message": "Event deleted"}

@router.get("/test")
def test_reload():
    return {"message": "Test reload working!"}
 