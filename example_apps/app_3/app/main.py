import stackprinter

from typing import Annotated

stackprinter.set_excepthook(style="darkbg2")

from dependencies import settings, api_settings, db_config, ENV, engine, SessionLocal
from dependencies import (
    create_base_metadata,
    get_engine,
    debug_metadata_obj,
    get_session,
)
from dependencies import saSQLiteConnection, Base, get_db
from sqlalchemy.orm import Session

from domain.item import Item, ItemCreate, ItemModel

from red_utils.loguru_utils import init_logger  # , fix_api_docs
from red_utils.fastapi_utils.src import healthcheck
from loguru import logger as log

from fastapi import Body, Depends, FastAPI, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

init_logger()

create_base_metadata(Base(), engine=engine)

ex_item_dict: dict = {"name": "Test", "description": "Test Item"}
log.info(f"[{ENV}] App Title: {settings.app_title}")

app = FastAPI(root_path="/api/v1", servers=[{"url": "/api/v1"}])

app.add_middleware(
    CORSMiddleware,
    allow_origins=api_settings.api_origins or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(healthcheck.router)


@app.get(
    "/",
    summary="Root path",
    description="An empty endpoint that simply returns a success response",
)
def hello_world():
    _content = {"message": "Hello world!"}
    content = JSONResponse(status_code=status.HTTP_200_OK, content=_content)

    return content


@app.post(
    "/items",
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
