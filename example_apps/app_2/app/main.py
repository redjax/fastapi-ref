from __future__ import annotations

from typing import Annotated

import stackprinter

stackprinter.set_excepthook(style="darkbg2")

from config import api_settings, settings
from dependencies import Base, get_engine, get_query_token, get_token_header
from fastapi import Body, Depends, FastAPI, Form, Header, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from loguru import logger as log
from red_utils.loguru_utils import init_logger
from routers import api_router

init_logger()

# log.info("Creating Base metadata")
# create_base_metadata(sqla_base, engine=sqla_engine)
engine = get_engine()
Base.metadata.create_all(engine)

## Initialize FastAPI app
app = FastAPI(dependencies=[Depends(get_query_token)])

app.add_middleware(
    CORSMiddleware,
    allow_origins=api_settings.api_origins or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router.router)


@app.get(
    "/",
    summary="Root path",
    description="An empty endpoint that simply returns a success response",
)
async def hello_world():
    _content = {"message": "Hello world!"}
    content = JSONResponse(status_code=status.HTTP_200_OK, content=content)

    return content
