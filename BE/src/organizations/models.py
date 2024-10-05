# CREATE TABLE IF NOT EXISTS "Organizations" (
# 	"UUID"	TEXT NOT NULL UNIQUE,
# 	"OrganizationName"	TEXT NOT NULL UNIQUE,
# 	"OrganizationAvatar"	TEXT,
# 	"OrganizationDescription"	TEXT,
# 	"OrganizationOwner"	TEXT NOT NULL,
# 	PRIMARY KEY("UUID"),
# 	FOREIGN KEY("OrganizationOwner") REFERENCES "Users"("UUID") ON DELETE CASCADE
# );


from pydantic import BaseModel
from typing import Optional


class Organization(BaseModel):
    UUID: str
    OrganizationName: str
    OrganizationAvatar: Optional[str]
    OrganizationDescription: str
    OrganizationOwner: str
    OrganizationUserCount: int


class OrganizationBody(BaseModel):
    OrganizationName: str
    OrganizationAvatar: Optional[str] = None
    OrganizationDescription: str


class OrganizationResponse(BaseModel):
    status: str
    organization_uuid: str
