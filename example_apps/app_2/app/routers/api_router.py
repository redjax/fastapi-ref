from fastapi import APIRouter
from routers import items, users

router = APIRouter()

router.include_router(items.router)
router.include_router(users.router)
