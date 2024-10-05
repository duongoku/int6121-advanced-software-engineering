from . import models
from dependencies import db_interact
import user_management.authentication

from fastapi import APIRouter, Depends, HTTPException

# CREATE TABLE IF NOT EXISTS "UserProfile" (
# 	"UUID"	TEXT NOT NULL UNIQUE,
# 	"UserEmail"	TEXT,
# 	"UserRealName"	TEXT,
# 	"UserAvatar"	BLOB NULL DEFAULT NULL,
# 	"UserPhoneNumber"	TEXT,
# 	"UserProfileRichContent"	TEXT,
# 	"UserProfileEducation"	TEXT,
# 	"UserProfileExperience"	TEXT,
# 	PRIMARY KEY("UUID"),
# 	FOREIGN KEY("UUID") REFERENCES "Users"("UUID") ON DELETE CASCADE,
# );

router = APIRouter(tags=["UserProfile"])


@router.get("/profile", response_model=models.UserProfile)
def profile(uuid: str):
    """
    Get user profile.
    """

    with db_interact.SQLiteContext() as db:
        user = db.execute(
            "SELECT * FROM Users WHERE UUID = ?",
            (uuid,),
        ).fetchone()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        profile = db.execute(
            "SELECT * FROM UserProfile WHERE UUID = ?",
            (uuid,),
        ).fetchone()

        if user["IsProfileVisible"] == False:
            # Only return the UUID, Real Name and Avatar, NULL everything else
            return models.UserProfile(
                UUID=profile["UUID"],
                UserEmail="",
                UserRealName=profile["UserRealName"],
                UserAvatar=user["UserAvatar"],
                UserPhoneNumber="",
                UserProfileRichContent="",
                UserProfileEducation="",
                UserProfileExperience="",
            )

        return models.UserProfile(
            UUID=profile["UUID"],
            UserEmail=profile["UserEmail"],
            UserRealName=profile["UserRealName"],
            UserAvatar=profile["UserAvatar"],
            UserPhoneNumber=profile["UserPhoneNumber"],
            UserProfileRichContent=profile["UserProfileRichContent"],
            UserProfileEducation=profile["UserProfileEducation"],
            UserProfileExperience=profile["UserProfileExperience"],
        )


@router.get("/me", response_model=models.UserProfile)
def me(token: str = Depends(user_management.authentication.oauth2_scheme)):
    """
    Get user's own profile.
    """

    with db_interact.SQLiteContext() as db:
        user = db.execute(
            "SELECT * FROM Users WHERE UserToken = ?",
            (token,),
        ).fetchone()

        if user is None:
            raise HTTPException(status_code=401, detail="Unauthorized")

        profile = db.execute(
            "SELECT * FROM UserProfile WHERE UUID = ?",
            (user["UUID"],),
        ).fetchone()

        return models.UserProfile(
            UUID=profile["UUID"],
            UserEmail=profile["UserEmail"],
            UserRealName=profile["UserRealName"],
            UserAvatar=profile["UserAvatar"],
            UserPhoneNumber=profile["UserPhoneNumber"],
            UserProfileRichContent=profile["UserProfileRichContent"],
            UserProfileEducation=profile["UserProfileEducation"],
            UserProfileExperience=profile["UserProfileExperience"],
        )


@router.put("/me", response_model=models.UserProfile)
def update_me(
    profile_body: models.UserProfileBody,
    token: str = Depends(user_management.authentication.oauth2_scheme),
):
    """
    Update user's own profile.
    """

    with db_interact.SQLiteContext() as db:
        user = db.execute(
            "SELECT * FROM Users WHERE UserToken = ?",
            (token,),
        ).fetchone()

        profile = db.execute(
            "SELECT * FROM UserProfile WHERE UUID = ?",
            (user["UUID"],),
        ).fetchone()

        if profile_body.UserEmail != "":
            db.execute(
                "UPDATE UserProfile SET UserEmail = ? WHERE UUID = ?",
                (profile_body.UserEmail, user["UUID"]),
            )

        if profile_body.UserRealName != "":
            db.execute(
                "UPDATE UserProfile SET UserRealName = ? WHERE UUID = ?",
                (profile_body.UserRealName, user["UUID"]),
            )

        if profile_body.UserAvatar != "":
            db.execute(
                "UPDATE UserProfile SET UserAvatar = ? WHERE UUID = ?",
                (profile_body.UserAvatar, user["UUID"]),
            )

        if profile_body.UserPhoneNumber != "":
            db.execute(
                "UPDATE UserProfile SET UserPhoneNumber = ? WHERE UUID = ?",
                (profile_body.UserPhoneNumber, user["UUID"]),
            )

        if profile_body.UserProfileRichContent != "":
            db.execute(
                "UPDATE UserProfile SET UserProfileRichContent = ? WHERE UUID = ?",
                (profile_body.UserProfileRichContent, user["UUID"]),
            )

        if profile_body.UserProfileEducation != "":
            db.execute(
                "UPDATE UserProfile SET UserProfileEducation = ? WHERE UUID = ?",
                (profile_body.UserProfileEducation, user["UUID"]),
            )

        if profile_body.UserProfileExperience != "":
            db.execute(
                "UPDATE UserProfile SET UserProfileExperience = ? WHERE UUID = ?",
                (profile_body.UserProfileExperience, user["UUID"]),
            )

        profile = db.execute(
            "SELECT * FROM UserProfile WHERE UUID = ?",
            (user["UUID"],),
        ).fetchone()

        return models.UserProfile(
            UUID=profile["UUID"],
            UserEmail=profile["UserEmail"],
            UserRealName=profile["UserRealName"],
            UserAvatar=profile["UserAvatar"],
            UserPhoneNumber=profile["UserPhoneNumber"],
            UserProfileRichContent=profile["UserProfileRichContent"],
            UserProfileEducation=profile["UserProfileEducation"],
            UserProfileExperience=profile["UserProfileExperience"],
        )


@router.get("/search", response_model=list[models.UserProfile])
def search(query: str, offset: int = 0, limit: int = 10):
    """
    Search for users.
    """
    with db_interact.SQLiteContext() as db:
        result = db.execute(
            """
            SELECT * FROM UserProfile
            WHERE UserProfileExperience LIKE ?
            OR UserProfileEducation LIKE ?
            OR UserRealName LIKE ?
            LIMIT ? OFFSET ?
            """,
            (f"%{query}%", f"%{query}%", f"%{query}%", limit, offset),
        ).fetchall()

        to_return = []

        for profile in result:
            to_return.append(
                models.UserProfile(
                    UUID=profile["UUID"],
                    UserEmail=profile["UserEmail"],
                    UserRealName=profile["UserRealName"],
                    UserAvatar=profile["UserAvatar"],
                    UserPhoneNumber=profile["UserPhoneNumber"],
                    UserProfileRichContent=profile["UserProfileRichContent"],
                    UserProfileEducation=profile["UserProfileEducation"],
                    UserProfileExperience=profile["UserProfileExperience"],
                )
            )

        return to_return
