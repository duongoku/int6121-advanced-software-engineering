from .registration import router as registration_router
from .deletion import router as deletion_router
from .authentication import router as authentication_router

from fastapi import APIRouter

router = APIRouter(prefix="/user", tags=["User Management"])

router.include_router(registration_router)
router.include_router(deletion_router)
router.include_router(authentication_router)
