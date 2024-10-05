import bcrypt
import datetime
import sqlite3
import uuid

from dependencies import db_interact
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

router = APIRouter()


class NewUser(BaseModel):
    real_name: str
    username: str
    email: str
    password: str


default_avatar = ""
with open("data/default_avatar.txt", "r") as f:
    default_avatar = f.read()


@router.post("/register")
def register(user: NewUser):
    """
    Register a new user.
    """

    real_name = user.real_name
    username = user.username
    email = user.email
    password = user.password

    if not real_name or not username or not password or not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please provide all required fields.",
        )

    with db_interact.SQLiteContext() as db:
        # Check if username is taken
        result = db.execute(
            "SELECT * FROM Users WHERE Username = ?",
            (username,),
        ).fetchone()
        if result:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username is already taken",
            )

        # Check if email is taken
        result = db.execute(
            "SELECT * FROM UserProfile WHERE UserEmail = ?",
            (email,),
        ).fetchone()
        if result:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email is already taken",
            )

        # Hash password
        hashed_password = bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt(),
        ).decode("utf-8")

        user_uuid = str(uuid.uuid4())

        # Create user
        db.execute(
            "INSERT INTO Users (UUID, Username, HashedPassword) VALUES (?, ?, ?)",
            (user_uuid, username, hashed_password),
        )

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
        # COMMIT;

        # Create a profile for the user
        db.execute(
            "INSERT INTO UserProfile (UUID, UserEmail, UserRealName, UserAvatar, UserPhoneNumber, UserProfileRichContent, UserProfileEducation, UserProfileExperience) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (user_uuid, email, real_name, default_avatar, "", "", "", ""),
        )

        return {"detail": "User created successfully", "success": True}
