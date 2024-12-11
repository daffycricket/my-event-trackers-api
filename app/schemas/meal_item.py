from pydantic import BaseModel, ConfigDict

class MealItemData(BaseModel):
    food_id: int
    quantity: float

# On garde MealItem identique à MealItemData car on ne renvoie pas plus d'infos
class MealItem(MealItemData):
    model_config = ConfigDict(from_attributes=True) 