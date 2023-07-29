import json

from pathlib import Path
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from loguru import logger as log

from domain.item import ItemModel, Item, ItemCreate
from dependencies import get_db, Session

router = APIRouter(prefix="/items", tags=["items"])


@router.post(
    "/",
    summary="Create a new Item",
    response_model=Item,
    response_model_exclude_unset=True,
    description="Create a new Item and add it to the database by converting the input ItemCreate schema into an ItemModel SQLAlchemy model.",
)
def post_create_item(item: ItemCreate, db: Session = Depends(get_db)):
    try:
        with db as client:
            db_user = client.query(ItemModel).where(ItemModel.name == item.name).first()

            if db_user:
                return JSONResponse(
                    status_code=400, content={"error": "Item already exists."}
                )
            else:
                new_item = ItemModel(name=item.name, description=item.description)
                db.add(new_item)
                db.commit()

                return new_item

    except Exception as exc:
        raise Exception(f"Unhandled exception creating Item. Details: {exc}")
