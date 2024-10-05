from fastapi import APIRouter
from .profile import router as profile_router


router = APIRouter(prefix="/profile")
router.include_router(profile_router)
