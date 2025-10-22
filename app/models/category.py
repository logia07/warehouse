from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base, item_category  # ← импортируем готовую таблицу

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)

    items = relationship("Item", secondary=item_category, back_populates="categories")