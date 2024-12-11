from typing import List, Optional
from uuid import UUID
import uuid
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, insert
from sqlalchemy.orm import selectinload

from app.database import get_db
from app.schemas.event import Event, EventCreate, EventUpdate
from app.models.event import Event as EventModel
from app.models import Food
from app.models.user import User
from app.auth.config import fastapi_users
from app.models.meal_item import MealItem as MealItemModel
from sqlalchemy.exc import IntegrityError
from app.schemas.meal_item import MealItem

router = APIRouter(
    prefix="/api/events",
    tags=["events"]
)

current_active_user = fastapi_users.current_user(active=True)

@router.get("", response_model=List[Event])
async def get_events(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(current_active_user)
):
    stmt = (
        select(EventModel)
        .where(EventModel.user_id == user.id)
        .options(
            selectinload(EventModel.meal_items).selectinload(MealItemModel.food)
        )
    )
    
    result = await db.execute(stmt)
    events = result.unique().scalars().all()
    
    return [
        Event(
            id=event.id,
            type=event.type,
            date=event.date,
            notes=event.notes,
            user_id=event.user_id,
            created_at=event.created_at,
            updated_at=event.updated_at,
            meal_items=[
                MealItem(
                    name=item.food.name,
                    quantity=item.quantity
                )
                for item in event.meal_items
            ]
        )
        for event in events
    ]

@router.post("", response_model=Event)
async def create_event(
    event: EventCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(current_active_user)
):
    # Créer l'event
    db_event = EventModel(
        type=event.type,
        date=event.date,
        notes=event.notes,
        user_id=user.id,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.add(db_event)
    await db.flush()

    # Si c'est un repas, gérer les meal_items
    if event.type == "MEAL" and event.meal_items:
        # Récupérer les foods par leur nom
        food_names = [item.name for item in event.meal_items]
        stmt = select(Food).where(Food.name.in_(food_names))
        result = await db.execute(stmt)
        foods = {food.name: food.id for food in result.scalars().all()}

        # Vérifier que tous les noms existent
        missing_foods = [name for name in food_names if name not in foods]
        if missing_foods:
            raise HTTPException(
                status_code=400,
                detail=f"Aliments non trouvés : {', '.join(missing_foods)}"
            )

        # Créer les meal_items
        for item in event.meal_items:
            await db.execute(
                insert(MealItemModel).values(
                    event_id=db_event.id,
                    food_id=foods[item.name],
                    quantity=item.quantity
                )
            )

    await db.commit()

    # Recharger l'event avec ses relations
    stmt = (
        select(EventModel)
        .where(EventModel.id == db_event.id)
        .options(
            selectinload(EventModel.meal_items).selectinload(MealItemModel.food)
        )
    )
    result = await db.execute(stmt)
    db_event = result.unique().scalar_one()

    # Convertir en schéma de réponse
    return Event(
        id=db_event.id,
        type=db_event.type,
        date=db_event.date,
        notes=db_event.notes,
        user_id=db_event.user_id,
        created_at=db_event.created_at,
        updated_at=db_event.updated_at,
        meal_items=[
            MealItem(
                name=item.food.name,
                quantity=item.quantity
            )
            for item in db_event.meal_items
        ] if db_event.meal_items else None
    )

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
    # Charger l'event avec ses relations en une seule requête
    stmt = (
        select(EventModel)
        .where(EventModel.id == event_id, EventModel.user_id == user.id)
        .options(
            selectinload(EventModel.meal_items).selectinload(MealItemModel.food)
        )
    )
    
    result = await db.execute(stmt)
    event = result.unique().scalar_one_or_none()
    
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    # Convertir explicitement en schéma de réponse
    return Event(
        id=event.id,
        type=event.type,
        date=event.date,
        notes=event.notes,
        user_id=event.user_id,
        created_at=event.created_at,
        updated_at=event.updated_at,
        meal_items=[
            MealItem(
                name=item.food.name,
                quantity=item.quantity
            )
            for item in event.meal_items
        ] if event.meal_items else None
    )

@router.put("/{event_id}", response_model=Event)
async def update_event(
    event_id: int,
    event_update: EventUpdate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(current_active_user)
):
    # Récupérer l'event existant avec ses relations
    stmt = (
        select(EventModel)
        .where(EventModel.id == event_id, EventModel.user_id == user.id)
        .options(
            selectinload(EventModel.meal_items).selectinload(MealItemModel.food)
        )
    )
    result = await db.execute(stmt)
    db_event = result.unique().scalar_one_or_none()
    
    if not db_event:
        raise HTTPException(status_code=404, detail="Event not found")

    # Mettre à jour les notes si fournies
    if event_update.notes is not None:
        db_event.notes = event_update.notes
        db_event.updated_at = datetime.utcnow()

    # Mettre à jour les meal_items si fournis
    if event_update.meal_items is not None:
        # Supprimer les anciens meal_items
        await db.execute(
            delete(MealItemModel).where(MealItemModel.event_id == event_id)
        )
        
        # Récupérer les foods par leur nom
        food_names = [item.name for item in event_update.meal_items]
        stmt = select(Food).where(Food.name.in_(food_names))
        result = await db.execute(stmt)
        foods = {food.name: food.id for food in result.scalars().all()}

        # Vérifier que tous les noms existent
        missing_foods = [name for name in food_names if name not in foods]
        if missing_foods:
            raise HTTPException(
                status_code=400,
                detail=f"Aliments non trouvés : {', '.join(missing_foods)}"
            )

        # Créer les nouveaux meal_items
        for item in event_update.meal_items:
            await db.execute(
                insert(MealItemModel).values(
                    event_id=event_id,
                    food_id=foods[item.name],
                    quantity=item.quantity
                )
            )

    await db.commit()

    # Recharger l'event avec ses relations mises à jour
    stmt = (
        select(EventModel)
        .where(EventModel.id == event_id)
        .options(
            selectinload(EventModel.meal_items).selectinload(MealItemModel.food)
        )
    )
    result = await db.execute(stmt)
    db_event = result.unique().scalar_one()

    # Convertir en schéma de réponse
    return Event(
        id=db_event.id,
        type=db_event.type,
        date=db_event.date,
        notes=db_event.notes,
        user_id=db_event.user_id,
        created_at=db_event.created_at,
        updated_at=db_event.updated_at,
        meal_items=[
            MealItem(
                name=item.food.name,
                quantity=item.quantity
            )
            for item in db_event.meal_items
        ] if db_event.meal_items else None
    )

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
 