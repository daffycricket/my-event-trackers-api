from sqlalchemy import Column, String, Integer, Enum, DateTime, func, Identity, Index, UniqueConstraint, Float, Table, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
import enum

class FoodCategory(str, enum.Enum):
    FRUITS = "fruits"
    VEGETABLES = "vegetables"
    PROTEINS = "proteins"
    CARBS = "carbs"
    DAIRY = "dairy"
    DRINKS = "drinks"
    SNACKS = "snacks"

class UnitType(str, enum.Enum):
    UNIT = "unit"
    WEIGHT = "weight"
    VOLUME = "volume"
    SERVING = "serving"
    SPOON = "spoon"

# Table d'association pour la relation many-to-many
meal_items = Table(
    'meal_items',
    Base.metadata,
    Column('event_id', ForeignKey('events.id'), primary_key=True),
    Column('food_id', ForeignKey('foods.name'), primary_key=True)
)

class Food(Base):
    __tablename__ = "foods"

    id = Column(Integer, Identity(), primary_key=True)
    name = Column(String, nullable=False)  # ex: "tomato"
    localized_label = Column(String, nullable=False)  # ex: "Tomate" ou "Tomato"
    language = Column(String, nullable=False)  # fr, en, etc.
    category = Column(Enum(FoodCategory), nullable=False)
    unit_type = Column(Enum(UnitType), nullable=False)
    default_quantity = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relation avec events
    events = relationship("Event", secondary="meal_items", back_populates="meal_items")

    # Index sur name et localized_label pour les recherches rapides
    __table_args__ = (
        Index('ix_foods_name', 'name'),
        Index('ix_foods_localized_label', 'localized_label'),
        UniqueConstraint('name', 'language', name='uq_foods_name_language'),
        UniqueConstraint('name', name='uq_food_name'),
    ) 