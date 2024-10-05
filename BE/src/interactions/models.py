# CREATE TABLE IF NOT EXISTS "Comments" (
# 	"CommentID"	TEXT NOT NULL UNIQUE,
# 	"CommentContent"	TEXT NOT NULL,
# 	"CommentOwner"	INTEGER NOT NULL,
# 	"CommentTimestamp"	INTEGER NOT NULL,
# 	"CommentLikes"	INTEGER DEFAULT 0,
# 	"CommentPost"	INTEGER NOT NULL,
# 	PRIMARY KEY("CommentID")
# );

# CREATE TABLE IF NOT EXISTS "Likes" (
# 	"LikeID"	TEXT NOT NULL UNIQUE,
# 	"LikeOwner"	INTEGER NOT NULL,
# 	"LikePost"	INTEGER NOT NULL,
# 	PRIMARY KEY("LikeID")
# );

from pydantic import BaseModel
from typing import Optional


class InteractionStatus(BaseModel):
    status: str
    post_uuid: str


class Like(BaseModel):
    LikeID: str
    LikeOwner: str
    LikeOwnerName: str
    LikeOwnerAvatar: Optional[str]
    LikePost: str


class Comment(BaseModel):
    CommentID: str
    CommentContent: str
    CommentOwner: str
    CommentOwnerName: str
    CommentOwnerAvatar: Optional[str]
    CommentTimestamp: float
    CommentPost: str


class CommentBody(BaseModel):
    CommentContent: str
    PostUUID: str
