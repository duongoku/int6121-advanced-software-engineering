# CREATE TABLE IF NOT EXISTS "UserProfile" (
# 	"UUID"	TEXT NOT NULL UNIQUE,
# 	"UserEmail"	TEXT,
# 	"UserRealName"	TEXT,
# 	"UserPhoneNumber"	TEXT,
# 	"UserProfileRichContent"	TEXT,
# 	"UserProfileEducation"	TEXT,
# 	"UserProfileExperience"	TEXT,
# 	PRIMARY KEY("UUID")
# );

from pydantic import BaseModel
from typing import Optional


class UserProfile(BaseModel):
    UUID: str
    UserEmail: str
    UserRealName: str
    UserAvatar: Optional[str]
    UserPhoneNumber: str
    UserProfileRichContent: str
    UserProfileEducation: str
    UserProfileExperience: str


class UserProfileBody(BaseModel):
    UserEmail: str
    UserRealName: str
    UserAvatar: Optional[str] = None
    UserPhoneNumber: str
    UserProfileRichContent: str
    UserProfileEducation: str
    UserProfileExperience: str
