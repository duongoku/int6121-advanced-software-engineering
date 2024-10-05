from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_contrib.permissions import PermissionsDependency

from dependencies import db_interact
from permissions import admin
from user_management import authentication
from . import models

router = APIRouter()


@router.post(
    "/disable_user",
    dependencies=[Depends(PermissionsDependency([admin.AdminPermission]))],
    response_model=models.AdminStatusResponse,
)
def disable_user(
    user_uuid: str,
    token: str = Depends(authentication.oauth2_scheme),
):
    """
    Disable a user. Must be admin.
    """

    with db_interact.SQLiteContext() as db:

        # Check if user exists
        user = db.execute(
            "SELECT * FROM Users WHERE UUID = ?",
            (user_uuid,),
        ).fetchone()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User does not exist",
            )

        # Disable user
        db.execute(
            "UPDATE Users SET IsUserActive = FALSE WHERE UUID = ?",
            (user_uuid,),
        )

        return models.AdminStatusResponse(
            status="ok", detail="User disabled successfully"
        )
