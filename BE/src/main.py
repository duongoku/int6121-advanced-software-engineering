from fastapi import APIRouter
from fastapi import FastAPI

app = FastAPI()

from user_management import router as user_management_router
from posts import router as posts_router
from user_profile import router as user_profile_router
from interactions import router as interactions_router
from organizations import router as organizations_router
from admin import router as admin_router
from auth import router as auth_router

router_with_prefix = APIRouter(prefix="/api")
router_with_prefix.include_router(user_management_router)
router_with_prefix.include_router(posts_router)
router_with_prefix.include_router(user_profile_router)
router_with_prefix.include_router(interactions_router)
router_with_prefix.include_router(organizations_router)
router_with_prefix.include_router(admin_router)
router_with_prefix.include_router(auth_router)

app.include_router(router_with_prefix)
