from fastapi import APIRouter, Depends, HTTPException, status
from dependencies import db_interact

import sqlite3
import datetime
import uuid

from user_management import authentication
from . import models

router = APIRouter(tags=["Posts Lifecycle"])

# CREATE TABLE IF NOT EXISTS "Posts" (
# 	"PostUUID"	TEXT NOT NULL UNIQUE,
# 	"PostTitle"	TEXT NOT NULL,
# 	"PostRichContent"	TEXT,
# 	"PostOwner"	INTEGER NOT NULL,
# 	"PostTimestamp"	INTEGER NOT NULL,
# 	PRIMARY KEY("PostID")
# );


@router.post("/new", response_model=models.PostStatus)
def new(
    post: models.MiniPostBody,
    token: str = Depends(authentication.oauth2_scheme),
) -> models.PostStatus:
    """
    Create a new post.
    """
    # Check if post name is taken
    with db_interact.SQLiteContext() as db:

        # get the user id from the token
        user_id = db.execute(
            "SELECT * FROM Users WHERE UserToken = ?",
            (token,),
        ).fetchone()["UUID"]

        # Check if the organization exist and under the user's ownership
        org = db.execute(
            "SELECT * FROM Organizations WHERE UUID = ? AND OrganizationOwner = ?",
            (post.PostOrganization, user_id),
        ).fetchone()

        if org is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Organization not found or not owned by user",
            )

        post_uuid = str(uuid.uuid4())

        # Insert the post into the database
        db.execute(
            "INSERT INTO Posts (PostUUID, PostTitle, PostRichContent, PostOwner, PostOrganization, PostTimestamp) VALUES (?, ?, ?, ?, ?, ?)",
            (
                post_uuid,
                post.PostTitle,
                post.PostRichContent,
                user_id,
                post.PostOrganization,
                datetime.datetime.now(),
            ),
        )

        ()
        return models.PostStatus(status="success", post_uuid=post_uuid)


@router.get("/{post_uuid}", response_model=models.Post)
def get_post(post_uuid: str) -> models.Post:
    """
    Get a post.
    """
    with db_interact.SQLiteContext() as db:

        # Get the post from the database
        post = db.execute(
            "SELECT * FROM Posts WHERE PostUUID = ?",
            (post_uuid,),
        ).fetchone()

        # Counts the likes and comments
        likes = db.execute(
            "SELECT COUNT(*) FROM Likes WHERE LikePost = ?",
            (post_uuid,),
        ).fetchone()[0]

        comments = db.execute(
            "SELECT COUNT(*) FROM Comments WHERE CommentPost = ?",
            (post_uuid,),
        ).fetchone()[0]

        owner_profile = db.execute(
            "SELECT UserRealName, UserAvatar FROM UserProfile WHERE UUID = ?",
            (post["PostOwner"],),
        ).fetchone()

        # calculate the seconds since the post was created
        converted_timestamp = datetime.datetime.strptime(
            post["PostTimestamp"], "%Y-%m-%d %H:%M:%S.%f"
        )
        seconds_since_post = (
            datetime.datetime.now() - converted_timestamp
        ).total_seconds()

        return models.Post(
            PostUUID=post["PostUUID"],
            PostTitle=post["PostTitle"],
            PostRichContent=post["PostRichContent"],
            PostOwner=post["PostOwner"],
            PostOwnerName=owner_profile["UserRealName"],
            PostOwnerAvatar=owner_profile["UserAvatar"],
            PostOrganization=post["PostOrganization"],
            PostTimestamp=seconds_since_post,
            PostLikes=likes,
            PostComments=comments,
        )


@router.post("/edit", response_model=models.PostStatus)
def edit(
    post_uuid: str,
    post_body: models.MiniPostBody,
    token: str = Depends(authentication.oauth2_scheme),
) -> models.PostStatus:
    """
    Edit a post.
    """
    # Check if post name is taken
    with db_interact.SQLiteContext() as db:

        # get the user id from the token
        user_id = db.execute(
            "SELECT * FROM Users WHERE UserToken = ?",
            (token,),
        ).fetchone()

        # If the post doesn't belong to the user, return an error
        post = db.execute(
            "SELECT * FROM Posts WHERE PostUUID = ?",
            (post_uuid,),
        ).fetchone()

        if post["PostOwner"] != user_id["UUID"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You do not own this post",
            )

        # Insert the post into the database
        db.execute(
            "UPDATE Posts SET PostTitle = ?, PostRichContent = ? WHERE PostUUID = ? AND PostOwner = ?",
            (
                post_body.PostTitle,
                post_body.PostRichContent,
                post_uuid,
                user_id["UUID"],
            ),
        )

        return models.PostStatus(status="success", post_uuid=post_uuid)


@router.post("/delete", response_model=models.PostStatus)
def delete(
    post_uuid: str,
    token: str = Depends(authentication.oauth2_scheme),
) -> models.PostStatus:
    """
    Delete a post.
    """
    with db_interact.SQLiteContext() as db:

        # get the user id from the token
        user_id = db.execute(
            "SELECT * FROM Users WHERE Token = ?",
            (token,),
        ).fetchone()

        # Insert the post into the database
        db.execute(
            "DELETE FROM Posts WHERE PostUUID = ? AND PostOwner = ?",
            (
                post_uuid,
                user_id,
            ),
        )

        ()
        return models.PostStatus(status="success", post_uuid=post_uuid)
