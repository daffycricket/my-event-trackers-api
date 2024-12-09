from fastapi import APIRouter, Query
from typing import List
from app.schemas import FoodItem

router = APIRouter()

@router.get("/foods", response_model=List[FoodItem])
async def get_food_items(language: str = Query("fr")):
    # Mock data
    if language == "fr":
        return [
            {
                "id": "tomato",
                "name": "Tomate",
                "category": "VEGETABLES",
                "unit_type": "UNIT",
                "default_quantity": 1
            },
            {
                "id": "chicken_breast",
                "name": "Blanc de poulet",
                "category": "PROTEINS",
                "unit_type": "GRAM",
                "default_quantity": 150
            },
            {
                "id": "olive_oil",
                "name": "Huile d'olive",
                "category": "CONDIMENTS",
                "unit_type": "TBSP",
                "default_quantity": 1
            }
        ]
    else:
        return [
            {
                "id": "tomato",
                "name": "Tomato",
                "category": "VEGETABLES",
                "unit_type": "UNIT",
                "default_quantity": 1
            },
            {
                "id": "chicken_breast",
                "name": "Chicken breast",
                "category": "PROTEINS",
                "unit_type": "GRAM",
                "default_quantity": 150
            },
            {
                "id": "olive_oil",
                "name": "Olive oil",
                "category": "CONDIMENTS",
                "unit_type": "TBSP",
                "default_quantity": 1
            }
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