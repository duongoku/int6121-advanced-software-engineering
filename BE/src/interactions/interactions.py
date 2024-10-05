import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from dependencies import db_interact
from user_management import authentication
from . import models

router = APIRouter(tags=["Interactions"])


@router.post("/like", response_model=models.InteractionStatus)
def like(post_uuid: str, token: str = Depends(authentication.oauth2_scheme)):
    """
    Like a post.
    """

    with db_interact.SQLiteContext() as db:

        # get the user id from the token
        user_id = db.execute(
            "SELECT * FROM Users WHERE UserToken = ?",
            (token,),
        ).fetchone()

        # Check if the user has already liked the post
        like = db.execute(
            "SELECT * FROM Likes WHERE LikeOwner = ? AND LikePost = ?",
            (user_id["UUID"], post_uuid),
        ).fetchone()

        if like:
            # Remove the like
            db.execute(
                "DELETE FROM Likes WHERE LikeOwner = ? AND LikePost = ?",
                (user_id["UUID"], post_uuid),
            )
            ()

        else:
            # Add the like
            db.execute(
                "INSERT INTO Likes (LikeOwner, LikePost) VALUES (?, ?)",
                (user_id["UUID"], post_uuid),
            )
            ()

        return models.InteractionStatus(status="success", post_uuid=post_uuid)


@router.post("/comment", response_model=models.InteractionStatus)
def comment(
    comment_body: models.CommentBody,
    token: str = Depends(authentication.oauth2_scheme),
):
    """
    Comment on a post.
    """

    with db_interact.SQLiteContext() as db:

        # get the user id from the token
        user_id = db.execute(
            "SELECT * FROM Users WHERE UserToken = ?",
            (token,),
        ).fetchone()

        # Add the comment
        db.execute(
            "INSERT INTO Comments (CommentOwner, CommentPost, CommentContent, CommentTimestamp) VALUES (?, ?, ?, ?)",
            (
                user_id["UUID"],
                comment_body.PostUUID,
                comment_body.CommentContent,
                datetime.datetime.now(),
            ),
        )
        ()

        return models.InteractionStatus(
            status="success", post_uuid=comment_body.PostUUID
        )


@router.get("/like", response_model=list[models.Like])
def get_likes(post_uuid: str):
    """
    Get all likes for a post.
    """

    with db_interact.SQLiteContext() as db:

        # Get the likes from the database
        likes = db.execute(
            "SELECT * FROM Likes WHERE LikePost = ?",
            (post_uuid,),
        ).fetchall()

        to_return = []

        for like in likes:
            owner_profile = db.execute(
                "SELECT UserRealName, UserAvatar FROM UserProfile WHERE UUID = ?",
                (like["LikeOwner"],),
            ).fetchone()

            to_return.append(
                models.Like(
                    LikeID=like["LikeID"],
                    LikeOwner=like["LikeOwner"],
                    LikeOwnerName=owner_profile["UserRealName"],
                    LikeOwnerAvatar=owner_profile["UserAvatar"],
                    LikePost=like["LikePost"],
                )
            )

        return to_return


@router.get("/comment", response_model=list[models.Comment])
def get_comments(post_uuid: str, limit: int = 10, offset: int = 0):
    """
    Get all comments for a post.
    """

    with db_interact.SQLiteContext() as db:

        # Get the comments from the database
        comments = db.execute(
            "SELECT * FROM Comments WHERE CommentPost = ? ORDER BY CommentTimestamp DESC LIMIT ? OFFSET ?",
            (post_uuid, limit, offset),
        ).fetchall()

        to_return = []

        for comment in comments:
            owner_profile = db.execute(
                "SELECT UserRealName, UserAvatar FROM UserProfile WHERE UUID = ?",
                (comment["CommentOwner"],),
            ).fetchone()

            # calculate the time since the comment was posted
            # convert the string back to a datetime object
            converted_timestamp = datetime.datetime.strptime(
                comment["CommentTimestamp"], "%Y-%m-%d %H:%M:%S.%f"
            )
            time_since = datetime.datetime.now() - converted_timestamp

            to_return.append(
                models.Comment(
                    CommentID=comment["CommentID"],
                    CommentOwner=comment["CommentOwner"],
                    CommentOwnerName=owner_profile["UserRealName"],
                    CommentOwnerAvatar=owner_profile["UserAvatar"],
                    CommentPost=comment["CommentPost"],
                    CommentContent=comment["CommentContent"],
                    CommentTimestamp=time_since.total_seconds(),
                )
            )

        return to_return
