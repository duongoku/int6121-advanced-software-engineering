import sqlite3
import bcrypt
import datetime
import jwt

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from dependencies import db_interact

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/delete")
def delete(username: str, password: str, token: str = Depends(oauth2_scheme)):
    """
    Delete a user.
    """
    # Check if username exists
    with db_interact.SQLiteContext() as db:
        result = db.execute(
            "SELECT * FROM Users WHERE Username = ?",
            (username,),
        ).fetchone()
        if not result:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username is not registered",
            )

        # Check password
        if not bcrypt.checkpw(
            password.encode("utf-8"),
            result["HashedPassword"].encode("utf-8"),
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incorrect password",
            )

        # Delete user
        db.execute(
            "DELETE FROM Users WHERE Username = ?",
            (username,),
        )

        return {"detail": "User deleted successfully"}
