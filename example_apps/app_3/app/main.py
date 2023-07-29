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

from red_utils.loguru_utils import init_logger
from red_utils.fastapi_utils import (
    healthcheck,
    fix_api_docs,
    tags_metadata,
    update_tags_metadata,
)
from loguru import logger as log

from fastapi import Body, Depends, FastAPI, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from routers import api_router

init_logger()

create_base_metadata(Base(), engine=engine)

new_metadata = {
    "name": "inventory",
    "description": "Interact with Items in a database. Demo CRUD operations.",
}
tags_metadata = update_tags_metadata(tags_metadata, update_metadata=new_metadata)

ex_item_dict: dict = {"name": "Test", "description": "Test Item"}
log.info(f"[{ENV}] App Title: {settings.app_title}")

app = FastAPI(
    tags_metadata=tags_metadata,
)
fix_api_docs(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=api_settings.api_origins or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(healthcheck.router)
app.include_router(api_router.router)


@app.get(
    "/",
    summary="Root path",
    description="An empty endpoint that simply returns a success response",
)
def hello_world():
    _content = {"message": "Hello world!"}
    content = JSONResponse(status_code=status.HTTP_200_OK, content=_content)

    return content
