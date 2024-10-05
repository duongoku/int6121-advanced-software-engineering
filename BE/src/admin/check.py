from fastapi import APIRouter, Depends, HTTPException, status
from permissions import admin
from fastapi_contrib.permissions import PermissionsDependency
from user_management import authentication
from dependencies import db_interact
from . import models

router = APIRouter()


@router.get(
    "/check",
    dependencies=[Depends(PermissionsDependency([admin.AdminPermission]))],
    response_model=models.AdminStatusResponse,
)
def check(token: str = Depends(authentication.oauth2_scheme)):
    """
    Check if user is admin. Must be admin.
    """

    return models.AdminStatusResponse(status="ok", detail="User is admin")
