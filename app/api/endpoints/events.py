from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime

from app.database import get_db
from app.schemas.event import Event, EventCreate, EventUpdate
from app.models import Event as EventModel, MealItem

router = APIRouter()

@router.get("/", response_model=List[Event])
def read_events(
    skip: int = 0,
    limit: int = 100,
    type: Optional[str] = Query(None, description="Filter by event type (meal/workout)"),
    from_date: Optional[datetime] = Query(None, description="Filter events from this date"),
    to_date: Optional[datetime] = Query(None, description="Filter events to this date"),
    db: Session = Depends(get_db)
):
    query = db.query(EventModel)
    
    if type:
        query = query.filter(EventModel.type == type)
    if from_date:
        query = query.filter(EventModel.date >= from_date)
    if to_date:
        query = query.filter(EventModel.date <= to_date)
    
    return query.order_by(EventModel.date.desc()).offset(skip).limit(limit).all()

@router.post("/", response_model=Event)
def create_event(event: EventCreate, db: Session = Depends(get_db)):
    event_data = event.model_dump()
    
    # Si c'est un événement de type MEAL, on extrait les meal_items
    if event_data["type"] == "MEAL" and "foods" in event_data["data"]:
        foods = event_data["data"].pop("foods", [])
        
        # Créer l'événement sans les foods
        db_event = EventModel(**event_data)
        db.add(db_event)
        
        # Ajouter les meal_items
        for food in foods:
            meal_item = MealItem(
                event=db_event,
                name=food["name"],
                quantity=food["quantity"]
            )
            db.add(meal_item)
    else:
        # Pour les autres types d'événements
        db_event = EventModel(**event_data)
        db.add(db_event)
    
    db.commit()
    db.refresh(db_event)
    return db_event

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