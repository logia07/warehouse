from typing import Literal
from pydantic import BaseModel
from pydantic.config import ConfigDict

RoleType = Literal["admin", "manager"]

class UserBase(BaseModel):
    username: str
    role: RoleType
    model_config = ConfigDict(from_attributes=True)

class UserCreate(BaseModel):
    username: str
    password: str
    role: RoleType = "manager"
    model_config = ConfigDict(from_attributes=True)

class UserLogin(BaseModel):
    username: str
    password: str
    model_config = ConfigDict(from_attributes=True)
