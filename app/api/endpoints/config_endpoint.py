from fastapi import APIRouter, Query, Depends
from typing import List
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.food import Food
from app.models.food import Food as FoodModel

router = APIRouter()

@router.get("/foods", response_model=List[Food])
async def get_food_items(
    language: str = Query("fr", description="Language code (fr, en, etc.)"),
    db: Session = Depends(get_db)
):
    # Récupérer les aliments de la base pour la langue demandée
    foods = db.query(FoodModel).filter(FoodModel.language == language).all()
    
    # Si aucun résultat, fallback sur le français
    if not foods and language != "fr":
        foods = db.query(FoodModel).filter(FoodModel.language == "fr").all()
    
    # Mapper les résultats selon le schéma attendu
    return [
        {
            "id": food.name,  # On utilise le champ 'name' comme identifiant
            "name": food.localized_label,  # Le nom localisé devient le nom affiché
            "category": food.category,
            "unit_type": food.unit_type,
            "default_quantity": food.default_quantity
        }
        for food in foods
    ]

@router.get("/timezones")
async def get_timezones():
    return {
        "timezones": [
            "Europe/Paris",
            "America/New_York",
            "Asia/Tokyo"
        ]
    }

@router.get("/app-version")
async def get_app_version():
    return {
        "min_version": "1.0.0",
        "latest_version": "1.2.0"
    } 