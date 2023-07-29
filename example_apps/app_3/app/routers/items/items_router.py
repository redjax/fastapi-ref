import json

from pathlib import Path
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from loguru import logger as log

from domain.item import ItemModel, Item, ItemCreate, crud
from dependencies import get_db, Session

router = APIRouter(prefix="/items", tags=["items"])


@router.get(
    "/all",
    summary="Return all Items from the database",
    response_model=list[Item],
    response_model_exclude_unset=True,
    description="Query database for all Items, return a list of Items.",
)
def get_all_items_in_db(db: Session = Depends(get_db)):
    db_items_success = crud.get_all_items(db=db)

    if not db_items_success:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"error": "Internal server error"},
        )

    return db_items_success


@router.get(
    "/name/{name}",
    summary="Search for an Item in the database by name.",
    response_model=Item,
    response_model_exclude_unset=True,
)
def get_item_by_name_in_db(name: str, db: Session = Depends(get_db)):
    db_item_success = crud.get_item_by_name(name=name, db=db)

    if not db_item_success:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content={"error": "Item not found"}
        )

    return db_item_success


@router.get(
    "/id/{id}",
    summary="Search for an Item in the database by ID.",
    response_model=Item,
    response_model_exclude_unset=True,
)
def get_item_by_id_in_db(id: int, db: Session = Depends(get_db)):
    db_item_success = crud.get_item_by_id(id=id, db=db)

    if not db_item_success:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content={"error": "Item not found"}
        )

    return db_item_success


@router.post(
    "/",
    summary="Create a new Item",
    response_model=Item,
    response_model_exclude_unset=True,
    description="Create a new Item and add it to the database by converting the input ItemCreate schema into an ItemModel SQLAlchemy model.",
)
def post_create_new_item(item: ItemCreate, db: Session = Depends(get_db)):
    db_item_success = crud.create_item(item, db=db)

    if not db_item_success:
        return JSONResponse(
            status_code=status.HTTP_304_NOT_MODIFIED,
            content={"info": "Item already exists."},
        )

    return db_item_success


@router.put("/id/{id}")
def update_item_in_db(id: int, item: ItemCreate, db: Session = Depends(get_db)):
    db_item_update_success = crud.update_item_by_id(id=id, item=item, db=db)

    if not db_item_update_success:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error": f"There was a problem updating Item with ID [{id}]."},
        )

    return db_item_update_success


@router.delete("/id/{id}", summary="Delete an Item from the database by ID.")
def delete_item_from_db(id: int, db: Session = Depends(get_db)):
    db_item_del_success = crud.delete_item_by_id(id=id, db=db)

    if not db_item_del_success:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"error": "Item not found, could not delete"},
        )

    return db_item_del_success
