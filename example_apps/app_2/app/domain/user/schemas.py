from __future__ import annotations

from .. import item_schemas

from pydantic import BaseModel

class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    items: list[item_schemas.Item] = []

    class Config:
        from_attributes = True
