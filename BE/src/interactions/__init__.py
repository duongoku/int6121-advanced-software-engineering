from fastapi import APIRouter
from .interactions import router as interactions_router

router = APIRouter(prefix="/interactions", tags=["Interactions"])
router.include_router(interactions_router)
