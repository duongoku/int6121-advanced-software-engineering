from fastapi import APIRouter, Depends, HTTPException

from dependencies import db_interact
from user_management import authentication
from . import models

router = APIRouter()

# CREATE TABLE IF NOT EXISTS "OrganizationMembers" (
# 	"OrganizationUUID"	TEXT NOT NULL,
# 	"UserUUID"	TEXT NOT NULL,
# 	"IsAdmin"	BOOL DEFAULT FALSE,
# 	PRIMARY KEY("OrganizationUUID","UserUUID"),
# 	FOREIGN KEY("OrganizationUUID") REFERENCES "Organizations"("UUID") ON DELETE CASCADE,
# 	FOREIGN KEY("UserUUID") REFERENCES "Users"("UUID") ON DELETE CASCADE
# );


@router.get("/mine", response_model=list[models.Organization])
def get_my_organizations(token: str = Depends(authentication.oauth2_scheme)):
    """
    Get all organizations that the user is a member of.
    """
    with db_interact.SQLiteContext() as db:

        # get the user id from the token
        user = db.execute(
            "SELECT * FROM Users WHERE UserToken = ?",
            (token,),
        ).fetchone()

        if not user:
            raise HTTPException(status_code=403, detail="Unauthorized")

        # Get all organizations that the user is a member of
        organizations = db.execute(
            "SELECT * FROM OrganizationMembers WHERE UserUUID = ?",
            (user["UUID"],),
        ).fetchall()

        organizations_details = [
            db.execute(
                "SELECT * FROM Organizations WHERE UUID = ?",
                (org["OrganizationUUID"],),
            ).fetchone()
            for org in organizations
        ]

        return [
            models.Organization(
                UUID=org["UUID"],
                OrganizationName=org["OrganizationName"],
                OrganizationAvatar=org["OrganizationAvatar"],
                OrganizationDescription=org["OrganizationDescription"],
                OrganizationOwner=org["OrganizationOwner"],
                OrganizationUserCount=db.execute(
                    "SELECT COUNT(*) FROM OrganizationMembers WHERE OrganizationUUID = ?",
                    (org["UUID"],),
                ).fetchone()[0],
            )
            for org in organizations_details
        ]


@router.get("/user", response_model=list[models.Organization])
def get_user_organizations(user_uuid: str):
    """
    Get all organizations that the user is a member of.
    """
    with db_interact.SQLiteContext() as db:

        # Get all organizations that the user is a member of
        organizations = db.execute(
            "SELECT * FROM OrganizationMembers WHERE UserUUID = ?",
            (user_uuid,),
        ).fetchall()

        organizations_details = [
            db.execute(
                "SELECT * FROM Organizations WHERE UUID = ?",
                (org["OrganizationUUID"],),
            ).fetchone()
            for org in organizations
        ]

        return [
            models.Organization(
                UUID=org["UUID"],
                OrganizationName=org["OrganizationName"],
                OrganizationAvatar=org["OrganizationAvatar"],
                OrganizationDescription=org["OrganizationDescription"],
                OrganizationOwner=org["OrganizationOwner"],
                OrganizationUserCount=db.execute(
                    "SELECT COUNT(*) FROM OrganizationMembers WHERE OrganizationUUID = ?",
                    (org["UUID"],),
                ).fetchone()[0],
            )
            for org in organizations_details
        ]
