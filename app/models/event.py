from sqlalchemy import Column, String, DateTime, JSON, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from app.database import Base
from app.models.food import Food

class Event(Base):
    __tablename__ = "events"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    type = Column(String, nullable=False)
    date = Column(DateTime, nullable=False)
    data = Column(JSON)
    notes = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)

    # Relation avec meal_items
    meal_items = relationship("Food", secondary="meal_items", back_populates="events")