from .lifecycle import router as lifecycle_router
from .listing import router as listing_router
from .application import router as application_router

from fastapi import APIRouter

router = APIRouter()

router.include_router(lifecycle_router, prefix="/post")
router.include_router(listing_router, prefix="/posts")
router.include_router(application_router, prefix="/post")
