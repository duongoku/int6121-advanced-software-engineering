# SCHEMA
# CREATE TABLE IF NOT EXISTS "Posts" (
# 	"PostID"	INTEGER,
# 	"PostTitle"	TEXT NOT NULL,
# 	"PostRichContent"	TEXT,
# 	"PostOwner"	INTEGER NOT NULL,
# 	"PostTimestamp"	INTEGER NOT NULL,
# 	"PostLikes"	TEXT,
# 	"PostComments"	TEXT,
# 	PRIMARY KEY("PostID" AUTOINCREMENT)
# );


# CREATE TABLE IF NOT EXISTS "Applications" (
# 	"UserUUID"	TEXT NOT NULL,
# 	"PostUUID"	TEXT NOT NULL,
# 	FOREIGN KEY("UserUUID") REFERENCES "Users"("UUID") ON DELETE CASCADE,
# 	FOREIGN KEY("PostUUID") REFERENCES "Posts"("PostUUID") ON DELETE CASCADE
# );

from pydantic import BaseModel
from typing import Optional


class Post(BaseModel):
    PostUUID: str
    PostTitle: str
    PostRichContent: str
    PostOwner: str
    PostOwnerName: str
    PostOwnerAvatar: Optional[str]
    PostOrganization: Optional[str]
    PostTimestamp: float
    PostLikes: int
    PostComments: int


class MiniPostBody(BaseModel):
    PostTitle: str
    PostRichContent: str
    PostOrganization: str


class PostStatus(BaseModel):
    status: str
    post_uuid: str


class Application(BaseModel):
    ApplicantUUID: str
    PostUUID: str


class ApplicationStatus(BaseModel):
    status: str
    ApplicantUUID: str
    PostUUID: str
