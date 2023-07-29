from __future__ import annotations

from config import api_settings
from fastapi import APIRouter, Depends, HTTPException
from loguru import logger as log

## Import sub-routers
# from routers.xxx import xxx_router
from red_utils.fastapi_utils import default_api_str, tags_metadata
from routers.items import items_router

prefix = api_settings.api_v1_path or "/api/v1"

router = APIRouter(
    prefix=prefix,
    responses={404: {"description": "Not found"}},
)

## Include sub-routers
# router.include_router(xxx_router.router)
router.include_router(items_router.router)
