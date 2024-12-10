from fastapi import APIRouter, Query, Depends
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.food import Food
from app.models.food import Food as FoodModel
from sqlalchemy import select

router = APIRouter()

@router.get("/foods", response_model=List[Food])
async def get_food_items(
    language: str = Query("fr", description="Language code (fr, en, etc.)"),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(FoodModel)
        .where(FoodModel.language == language)
    )
    foods = result.scalars().all()
    
    return [
        {
            "id": food.name,
            "name": food.localized_label,
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