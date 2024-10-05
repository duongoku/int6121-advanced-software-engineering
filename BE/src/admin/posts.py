from fastapi import APIRouter, Depends, HTTPException, status
from permissions import admin
from fastapi_contrib.permissions import PermissionsDependency
from user_management import authentication
from dependencies import db_interact
from . import models

router = APIRouter()


@router.post(
    "/delete_post",
    dependencies=[Depends(PermissionsDependency([admin.AdminPermission]))],
    response_model=models.AdminStatusResponse,
)
def delete_post(
    post_uuid: str,
    token: str = Depends(authentication.oauth2_scheme),
):
    """
    Forcefully delete a post regardless of the user. Must be admin.
    """

    with db_interact.SQLiteContext() as db:

        # Check if post exists
        post = db.execute(
            "SELECT * FROM Posts WHERE UUID = ?",
            (post_uuid,),
        ).fetchone()
        if not post:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Post does not exist",
            )

        # Delete post
        db.execute(
            "DELETE FROM Posts WHERE UUID = ?",
            (post_uuid,),
        )

        return models.AdminStatusResponse(
            status="ok", detail="Post deleted successfully"
        )
