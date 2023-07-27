from pydantic import BaseModel, Field


class ItemBase(BaseModel):
    name: str | None = Field(
        default=None,
        title="Item's name",
        examples=["example", "Example", "example_item", "ExampleItem"],
    )
    description: str | None = Field(
        default=None,
        title="Item's description",
        examples=["This is an example description of an Item"],
    )
    price: float | None = Field(
        default=0.00, title="Item's price", examples=[1.00, 150.00, 10000.00]
    )
    tax: float = Field(
        default=10.5, title="Item's tax percetnage", examples=[0.5, 2.5, 10, 12.0]
    )
    tags: set[str] = Field(
        default=set(), title="Item's tags", examples=["tag1", "tag2", "tag3"]
    )


class Item(ItemBase):
    pass
