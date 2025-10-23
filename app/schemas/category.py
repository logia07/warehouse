from pydantic import BaseModel
from pydantic.config import ConfigDict

class CategoryBase(BaseModel):
    id: int
    name: str
    class Config:
        from_attributes = True
