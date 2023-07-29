from __future__ import annotations

from .schemas import Item, ItemCreate
from .models import ItemModel

from sqlalchemy.orm import Session


def validate_db(db: Session = None) -> Session:
    if not db:
        raise ValueError("Missing DB Session object")

    if not isinstance(db, Session):
        raise TypeError(
            f"Invalid type for db: ({type(db)}). Must be of type sqlalchemy.orm.Session"
        )

    return db


def validate_item_create(item) -> ItemCreate:
    if not item:
        raise ValueError("Missing Item to add to database")

    if not isinstance(item, ItemCreate):
        raise TypeError(
            f"Invalid type for item: ({type(item)}). Must be of type ItemCreate"
        )

    return item


def create_item(item: ItemCreate = None, db: Session = None):
    validate_item_create(item)
    validate_db(db)

    try:
        with db as sess:
            db_user = sess.query(ItemModel).where(ItemModel.name == item.name).first()

            if db_user:
                return False
            else:
                new_item = ItemModel(**item.model_dump())
                sess.add(new_item)
                sess.commit()

                return new_item

    except Exception as exc:
        raise Exception(f"Unhandled exception creating Item. Details: {exc}")


def get_all_items(db: Session = None):
    validate_db(db)

    try:
        with db as sess:
            all_items = sess.query(ItemModel).all()

            return all_items

    except Exception as exc:
        raise Exception(f"Unhandled exception getting all Items. Details: {exc}")


def get_item_by_name(name: str = None, db: Session = None) -> Item:
    if not name:
        raise ValueError("Missing a name to search")

    if not isinstance(name, str):
        raise ValueError(f"Invalid type for name: {type(name)}. Must be of type str")

    try:
        with db as sess:
            db_item = sess.query(ItemModel).where(ItemModel.name == name).first()

            return db_item

    except Exception as exc:
        raise Exception(
            f"Unhandled exception retrieving Item by name '{name}'. Details: {exc}"
        )


def get_item_by_id(id: int = None, db: Session = None) -> Item:
    if not id:
        raise ValueError("Missing an ID to search")

    if not isinstance(id, int):
        raise ValueError(f"Invalid type for id: {type(id)}. Must be of type int")

    try:
        with db as sess:
            db_item = sess.query(ItemModel).where(ItemModel.id == id).first()

            return db_item

    except Exception as exc:
        raise Exception(
            f"Unhandled exception retrieving Item by ID '{id}'. Details: {exc}"
        )


def update_item_by_id(id: int = None, item: Item = None, db: Session = None):
    if not id:
        raise ValueError("Missing ID to search")

    if not isinstance(id, int):
        raise TypeError(f"Invalid type for ID: {type(id)}. Must be of type int")

    validate_db(db)

    with db as sess:
        db_item = sess.query(ItemModel).filter(ItemModel.id == id).first()

        if not db_item:
            return None

        update_data = item.model_dump(exclude_unset=True)

        sess.query(ItemModel).filter(ItemModel.id == id).update(
            update_data, synchronize_session=False
        )

        sess.commit()
        sess.refresh(db_item)

    return db_item


def delete_item_by_id(id: int = None, db: Session = None):
    try:
        with db as sess:
            db_item = sess.query(ItemModel).filter(ItemModel.id == id).first()

            if not db_item:
                return None

            _del = sess.query(ItemModel).filter(ItemModel.id == id).delete()

            sess.commit()

            return {"success": f"Deleted Item with ID: {id}"}

    except Exception as exc:
        raise Exception(
            f"Unhandled exception deleting Item with ID: {id}. Details: {exc}"
        )
