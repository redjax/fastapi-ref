from pydantic import BaseModel, Field


class ItemBase(BaseModel):
    name: str = Field(default=None, description="The name of the Item")
    description: str = Field(default=None, description="The description of the Item")


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int

    class Config:
        from_attributes = True
