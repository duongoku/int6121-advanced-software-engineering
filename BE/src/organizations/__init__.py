from .lifecycle import router as lifecycle_router
from .listing import router as listing_router
from fastapi import APIRouter

router = APIRouter(prefix="/orgs", tags=["Organizations"])

router.include_router(lifecycle_router)
router.include_router(listing_router)
