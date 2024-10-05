from .posts import router as posts_router
from .users import router as users_router
from .interactions import router as interactions_router
from .check import router as check_router

from fastapi import APIRouter

router = APIRouter(prefix="/admin", tags=["Administration"])

router.include_router(posts_router)
router.include_router(users_router)
router.include_router(interactions_router)
router.include_router(check_router)
