from __future__ import annotations
from pydantic import BaseModel, field_validator
from typing import List
from .category import CategoryBase  # ← относительный импорт

class ItemBase(BaseModel):
    id: int
    name: str
    price: float
    quantity: int
    categories: List[CategoryBase] = []

    model_config = {"from_attributes": True}

class ItemCreate(BaseModel):
    name: str
    price: float
    quantity: int
    category_ids: List[int] = []

    @field_validator("price")
    @classmethod
    def price_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("Цена должна быть больше 0")
        return v

    @field_validator("quantity")
    @classmethod
    def quantity_must_be_non_negative(cls, v):
        if v < 0:
            raise ValueError("Количество не может быть отрицательным")
        return v

class ItemUpdate(ItemCreate):
    pass

# ВАЖНО: rebuild после всех объявлений
ItemBase.model_rebuild()
