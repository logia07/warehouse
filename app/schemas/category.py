from __future__ import annotations
from pydantic import BaseModel
from pydantic.config import ConfigDict

class CategoryBase(BaseModel):
    id: int
    name: str

model_config = ConfigDict(from_attributes=True)
