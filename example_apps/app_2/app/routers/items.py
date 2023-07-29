from __future__ import annotations

from dependencies import get_db, get_token_header
from domain.item import (
    models as item_models,
    schemas as item_schemas,
)
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

fake_items_db = {"plumbus": {"name": "Plumbus"}, "gun": {"name": "Portal Gun"}}

router = APIRouter(
    prefix="/items",
    tags=["items"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def read_items():
    return fake_items_db


@router.post("/items/", response_model=item_schemas.Item)
def create_item(item: item_schemas.Item, db: Session = Depends(get_db)):
    with db as client:
        db_user = (
            client.query(item_schemas.Item)
            .where(item_schemas.Item.title == item.title)
            .first()
        )

        if db_user:
            raise HTTPException(status_code=400, detail="Item already created.")
