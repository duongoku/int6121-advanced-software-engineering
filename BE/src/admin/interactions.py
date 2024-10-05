from fastapi import APIRouter, Depends, HTTPException, status
from permissions import admin
from fastapi_contrib.permissions import PermissionsDependency
from user_management import authentication
from dependencies import db_interact
from . import models

router = APIRouter()


@router.post(
    "/delete_comment",
    dependencies=[Depends(PermissionsDependency([admin.AdminPermission]))],
    response_model=models.AdminStatusResponse,
)
def delete_comment(
    comment_uuid: str,
    token: str = Depends(authentication.oauth2_scheme),
):
    """
    Forcefully delete a comment regardless of the user. Must be admin.
    """

    with db_interact.SQLiteContext() as db:

        # Check if comment exists
        comment = db.execute(
            "SELECT * FROM Comments WHERE UUID = ?",
            (comment_uuid,),
        ).fetchone()
        if not comment:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Comment does not exist",
            )

        # Delete comment
        db.execute(
            "DELETE FROM Comments WHERE UUID = ?",
            (comment_uuid,),
        )

        return models.AdminStatusResponse(
            status="ok", detail="Comment deleted successfully"
        )
