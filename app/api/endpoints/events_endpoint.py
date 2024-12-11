from typing import List, Optional
from uuid import UUID
import uuid
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from app.database import get_db
from app.schemas.event import Event, EventCreate, EventUpdate
from app.models import Event as EventModel, Food
from app.models.user import User
from app.auth.config import fastapi_users
from app.models.meal_item import MealItem
from sqlalchemy.exc import IntegrityError

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
    db_event = EventModel(
        type=event.type,
        date=event.date,
        notes=event.notes,
        user_id=user.id,
        created_at=now,
        updated_at=now
    )
    db.add(db_event)
    await db.flush()  # Pour obtenir l'ID de l'event

    # Si c'est un repas, gérer les meal_items
    if event.type == "MEAL" and event.meal_items:
        # Vérifier que tous les food_id existent
        food_ids = [item.food_id for item in event.meal_items]
        foods = await db.execute(select(Food).where(Food.id.in_(food_ids)))
        existing_foods = {food.id for food in foods.scalars().all()}
        
        if not all(food_id in existing_foods for food_id in food_ids):
            await db.rollback()
            raise HTTPException(status_code=400, detail="Invalid food_id referenced")

        # Créer les meal_items
        try:
            for item in event.meal_items:
                meal_item = MealItem(
                    event_id=db_event.id,
                    food_id=item.food_id,
                    quantity=item.quantity
                )
                db.add(meal_item)
        except IntegrityError:
            await db.rollback()
            raise HTTPException(status_code=400, detail="Duplicate food in meal")

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
async def get_event(
    event_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(current_active_user)
):
    event = await db.get(EventModel, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    if event.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this event")
    return event

@router.put("/{event_id}", response_model=Event)
async def update_event(
    event_id: int,
    event_update: EventUpdate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(current_active_user)
):
    # Récupérer l'event existant
    event = await db.get(EventModel, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    if event.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized to modify this event")

    # Mettre à jour les champs simples
    if event_update.notes is not None:
        event.notes = event_update.notes
    if event_update.date is not None:
        event.date = event_update.date
    if event_update.type is not None:
        event.type = event_update.type

    # Mettre à jour les meal_items
    if event_update.meal_items is not None:
        # Supprimer les anciens meal_items
        await db.execute(
            delete(MealItem).where(MealItem.event_id == event_id)
        )
        
        # Créer les nouveaux meal_items
        for item in event_update.meal_items:
            db_meal_item = MealItem(
                event_id=event_id,
                food_id=item.food_id,
                quantity=item.quantity
            )
            db.add(db_meal_item)

    await db.commit()
    await db.refresh(event)
    return event

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
 