from fastapi import APIRouter, Depends, HTTPException
from dependencies import db_interact

from user_management import authentication
from . import models

router = APIRouter(tags=["Post Application"])


@router.post("/{post_uuid}/apply", response_model=models.ApplicationStatus)
def apply_to_post(post_uuid: str, token: str = Depends(authentication.oauth2_scheme)):
    """
    Apply to a post
    """
    with db_interact.SQLiteContext() as db:

        # get the user id from the token
        user = db.execute(
            "SELECT * FROM Users WHERE UserToken = ?",
            (token,),
        ).fetchone()

        # Check if the post exists
        post = db.execute(
            "SELECT * FROM Posts WHERE PostUUID = ?",
            (post_uuid,),
        ).fetchone()

        if not post:
            raise HTTPException(status_code=404, detail="Post not found")

        # Check if the user has already applied to the post
        application = db.execute(
            "SELECT * FROM Applications WHERE PostUUID = ? AND ApplicantUUID = ?",
            (post_uuid, user["UUID"]),
        ).fetchone()

        if application:
            raise HTTPException(
                status_code=400, detail="User has already applied to this post"
            )

        # Create the application
        db.execute(
            "INSERT INTO Applications (PostUUID, ApplicantUUID) VALUES (?, ?)",
            (
                post_uuid,
                user["UUID"],
            ),
        )

        return models.ApplicationStatus(
            status="success", PostUUID=post_uuid, ApplicantUUID=user["UUID"]
        )


@router.get("/{post_uuid}/applications", response_model=list[models.Application])
def get_applications(
    post_uuid: str, token: str = Depends(authentication.oauth2_scheme)
):
    """
    Get all applications for a post
    """
    with db_interact.SQLiteContext() as db:
        # get the user id from the token
        user = db.execute(
            "SELECT * FROM Users WHERE UserToken = ?",
            (token,),
        ).fetchone()

        # Check if the user is the owner of the post
        post = db.execute(
            "SELECT * FROM Posts WHERE PostUUID = ?",
            (post_uuid,),
        ).fetchone()

        if post["PostOwner"] != user["UUID"]:
            raise HTTPException(
                status_code=403, detail="User is not the owner of this post"
            )

        # Get all applications for the post
        applications = db.execute(
            "SELECT * FROM Applications WHERE PostUUID = ?",
            (post_uuid,),
        ).fetchall()

        return [models.Application(**application) for application in applications]
