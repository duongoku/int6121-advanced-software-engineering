from fastapi import APIRouter, Depends, HTTPException

from dependencies import db_interact
from . import models

import datetime

router = APIRouter(tags=["Posts Listings"])


@router.get("/all", response_model=list[models.Post])
def all(offset: int = 0, limit: int = 10):
    """
    Get all posts.
    """
    with db_interact.SQLiteContext() as db:
        result = db.execute(
            "SELECT * FROM Posts ORDER BY PostTimestamp DESC LIMIT ? OFFSET ?",
            (limit, offset),
        ).fetchall()

        to_return = []

        for post in result:
            # Count the number of likes
            likes = db.execute(
                "SELECT COUNT(*) FROM Likes WHERE LikePost = ?",
                (post["PostUUID"],),
            ).fetchone()[0]

            # Count the number of comments
            comments = db.execute(
                "SELECT COUNT(*) FROM Comments WHERE CommentPost = ?",
                (post["PostUUID"],),
            ).fetchone()[0]

            owner_profile = db.execute(
                "SELECT UserRealName, UserAvatar FROM UserProfile WHERE UUID = ?",
                (post["PostOwner"],),
            ).fetchone()

            # calculate the seconds since the post was created
            # convert the string back to a datetime object
            converted_timestamp = datetime.datetime.strptime(
                post["PostTimestamp"], "%Y-%m-%d %H:%M:%S.%f"
            )
            seconds_since_post = datetime.datetime.now() - converted_timestamp

            to_return.append(
                models.Post(
                    PostUUID=post["PostUUID"],
                    PostTitle=post["PostTitle"],
                    PostRichContent=post["PostRichContent"],
                    PostOwner=post["PostOwner"],
                    PostOwnerName=owner_profile["UserRealName"],
                    PostOwnerAvatar=owner_profile["UserAvatar"],
                    PostOrganization=post["PostOrganization"],
                    PostTimestamp=seconds_since_post.total_seconds(),
                    PostLikes=likes,
                    PostComments=comments,
                )
            )

        if len(to_return) == 0:
            return []
        return to_return


@router.get("/search", response_model=list[models.Post])
def search(query: str, offset: int = 0, limit: int = 10):
    """
    Search for posts.
    """
    with db_interact.SQLiteContext() as db:
        result = db.execute(
            "SELECT * FROM Posts WHERE PostTitle LIKE ? ORDER BY PostTimestamp DESC LIMIT ? OFFSET ?",
            (f"%{query}%", limit, offset),
        ).fetchall()

        to_return = []

        for post in result:
            # Count the number of likes
            likes = db.execute(
                "SELECT COUNT(*) FROM Likes WHERE LikePost = ?",
                (post["PostUUID"],),
            ).fetchone()[0]

            # Count the number of comments
            comments = db.execute(
                "SELECT COUNT(*) FROM Comments WHERE CommentPost = ?",
                (post["PostUUID"],),
            ).fetchone()[0]

            owner_profile = db.execute(
                "SELECT UserRealName, UserAvatar FROM UserProfile WHERE UUID = ?",
                (post["PostOwner"],),
            ).fetchone()

            # calculate the seconds since the post was created
            # convert the string back to a datetime object
            converted_timestamp = datetime.datetime.strptime(
                post["PostTimestamp"], "%Y-%m-%d %H:%M:%S.%f"
            )
            seconds_since_post = datetime.datetime.now() - converted_timestamp

            # get the organization name
            org_names = db.execute(
                "SELECT OrganizationName FROM Organizations WHERE OrganizationOwner = ?",
                (post["PostOwner"],),
            ).fetchall()

            to_return.append(
                models.Post(
                    PostUUID=post["PostUUID"],
                    PostTitle=post["PostTitle"],
                    PostRichContent=post["PostRichContent"],
                    PostOwner=post["PostOwner"],
                    PostOwnerName=owner_profile["UserRealName"],
                    PostOwnerAvatar=owner_profile["UserAvatar"],
                    PostOwnerOrganization=", ".join([org[0] for org in org_names]),
                    PostTimestamp=seconds_since_post.total_seconds(),
                    PostLikes=likes,
                    PostComments=comments,
                )
            )

        return to_return
