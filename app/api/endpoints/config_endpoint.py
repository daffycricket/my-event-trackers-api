from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.database import get_db
from app.models.food import Food as FoodModel
from app.models.label import Label
from app.schemas.food import Food as FoodSchema

router = APIRouter(
    prefix="/api/config",
    tags=["config"]
)

@router.get("/foods", response_model=List[FoodSchema])
async def get_foods(language: str = "fr", db: AsyncSession = Depends(get_db)):
    # D'abord récupérer tous les foods
    result = await db.execute(select(FoodModel))
    foods = result.scalars().all()
    
    # Puis récupérer leurs labels dans la langue demandée
    for food in foods:
        label_result = await db.execute(
            select(Label)
            .where(
                Label.entity_type == "food",
                Label.entity_id == food.id,
                Label.language == language
            )
        )
        label = label_result.scalar_one_or_none()
        if label:
            food.label = label.value
    
    return foods 