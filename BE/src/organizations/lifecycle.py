from fastapi import APIRouter, Depends, HTTPException
from . import models
import uuid

from dependencies import db_interact
from user_management import authentication

router = APIRouter()

# CREATE TABLE IF NOT EXISTS "OrganizationMembers" (
# 	"OrganizationUUID"	TEXT NOT NULL,
# 	"UserUUID"	TEXT NOT NULL,
# 	"IsAdmin"	BOOL DEFAULT FALSE,
# 	PRIMARY KEY("OrganizationUUID","UserUUID"),
# 	FOREIGN KEY("OrganizationUUID") REFERENCES "Organizations"("UUID") ON DELETE CASCADE,
# 	FOREIGN KEY("UserUUID") REFERENCES "Users"("UUID") ON DELETE CASCADE
# );


@router.post("/create", response_model=models.Organization)
async def create_organization(
    org_body: models.OrganizationBody,
    token: str = Depends(authentication.oauth2_scheme),
):
    """
    Create an organization based on user
    """
    with db_interact.SQLiteContext() as db:

        # get the user id from the token
        user = db.execute(
            "SELECT * FROM Users WHERE UserToken = ?",
            (token,),
        ).fetchone()

        # Create the organization
        org_uuid = str(uuid.uuid4())

        db.execute(
            "INSERT INTO Organizations (UUID, OrganizationName, OrganizationAvatar, OrganizationDescription, OrganizationOwner) VALUES (?, ?, ?, ?, ?)",
            (
                org_uuid,
                org_body.OrganizationName,
                org_body.OrganizationAvatar,
                org_body.OrganizationDescription,
                user["UUID"],
            ),
        )

        # Associate the user with the new organization

        db.execute(
            "INSERT INTO OrganizationMembers (OrganizationUUID, UserUUID, IsAdmin) VALUES (?, ?, ?)",
            (
                org_uuid,
                user["UUID"],
                True,
            ),
        )

        return models.Organization(
            UUID=org_uuid,
            OrganizationName=org_body.OrganizationName,
            OrganizationOwner=user["UUID"],
            OrganizationAvatar=org_body.OrganizationAvatar,
            OrganizationDescription=org_body.OrganizationDescription,
            OrganizationUserCount=1,
        )


@router.post("/join", response_model=models.OrganizationResponse)
def join_organization(
    org_uuid: str,
    token: str = Depends(authentication.oauth2_scheme),
):
    """
    Join an organization based on user
    """
    with db_interact.SQLiteContext() as db:

        # get the user id from the token
        user = db.execute(
            "SELECT * FROM Users WHERE UserToken = ?",
            (token,),
        ).fetchone()

        # Check if the organization exists
        org = db.execute(
            "SELECT * FROM Organizations WHERE UUID = ?",
            (org_uuid,),
        ).fetchone()

        if not org:
            raise HTTPException(status_code=404, detail="Organization does not exist")

        # Associate the user with the new organization
        db.execute(
            "INSERT INTO OrganizationMembers (OrganizationUUID, UserUUID, IsAdmin) VALUES (?, ?, ?)",
            (
                org_uuid,
                user["UUID"],
                False,
            ),
        )

        return models.OrganizationResponse(
            status="success",
            organization_uuid=org_uuid,
        )


@router.post("/leave", response_model=models.OrganizationResponse)
def leave_organization(
    org_uuid: str,
    token: str = Depends(authentication.oauth2_scheme),
):
    """
    Leave an organization based on user
    """
    with db_interact.SQLiteContext() as db:

        # get the user id from the token
        user = db.execute(
            "SELECT * FROM Users WHERE UserToken = ?",
            (token,),
        ).fetchone()

        # Remove the user from the organization
        db.execute(
            "DELETE FROM OrganizationMembers WHERE OrganizationUUID = ? AND UserUUID = ?",
            (
                org_uuid,
                user["UUID"],
            ),
        )

        # If the user is the owner of the organization, delete the organization
        org = db.execute(
            "SELECT * FROM Organizations WHERE UUID = ? AND OrganizationOwner = ?",
            (
                org_uuid,
                user["UUID"],
            ),
        ).fetchone()

        if org:
            db.execute(
                "DELETE FROM Organizations WHERE UUID = ?",
                (org_uuid,),
            )

        return models.OrganizationResponse(
            status="success",
            organization_uuid=org_uuid,
        )


@router.get("/get", response_model=models.Organization)
def get_organization(org_uuid: str):
    """
    Get an organization based on user
    """
    with db_interact.SQLiteContext() as db:

        # Get the organization
        org = db.execute(
            "SELECT * FROM Organizations WHERE UUID = ?", (org_uuid,)
        ).fetchone()

        # count the users in the organization
        user_count = db.execute(
            "SELECT COUNT(*) FROM OrganizationMembers WHERE OrganizationUUID = ?",
            (org_uuid,),
        ).fetchone()

        return models.Organization(
            UUID=org["UUID"],
            OrganizationName=org["OrganizationName"],
            OrganizationOwner=org["OrganizationOwner"],
            OrganizationAvatar=org["OrganizationAvatar"],
            OrganizationDescription=org["OrganizationDescription"],
            OrganizationUserCount=user_count[0],
        )


@router.put("/edit", response_model=models.Organization)
def edit_organization(
    org_uuid: str,
    org_body: models.OrganizationBody,
    token: str = Depends(authentication.oauth2_scheme),
):
    """
    Edit an organization based on user
    """

    # Check if the user is the owner of the organization
    with db_interact.SQLiteContext() as db:

        # get the user id from the token
        user = db.execute(
            "SELECT * FROM Users WHERE UserToken = ?",
            (token,),
        ).fetchone()

        # Check if the user's uuid is already associated with an organization
        org = db.execute(
            "SELECT * FROM Organizations WHERE UUID = ? AND OrganizationOwner = ?",
            (org_uuid, user["UUID"]),
        ).fetchone()

        if not org:
            raise HTTPException(
                status_code=400, detail="User is not the owner of the organization"
            )

        # Edit the organization
        if org_body.OrganizationName != "":
            db.execute(
                "UPDATE Organizations SET OrganizationName = ? WHERE UUID = ?",
                (org_body.OrganizationName, org_uuid),
            )

        if org_body.OrganizationAvatar != "":
            db.execute(
                "UPDATE Organizations SET OrganizationAvatar = ? WHERE UUID = ?",
                (org_body.OrganizationAvatar, org_uuid),
            )

        if org_body.OrganizationDescription != "":
            db.execute(
                "UPDATE Organizations SET OrganizationDescription = ? WHERE UUID = ?",
                (org_body.OrganizationDescription, org_uuid),
            )

        ()

        return models.Organization(
            org_uuid=org_uuid,
            org_name=org_body.OrganizationName,
            org_avatar=org_body.OrganizationAvatar,
            org_description=org_body.OrganizationDescription,
            org_owner=user["UUID"],
        )
