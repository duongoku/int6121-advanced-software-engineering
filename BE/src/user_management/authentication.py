import bcrypt
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from dependencies import db_interact
from dependencies.constants import ALGORITHM, SECRET_KEY
import jwt
from .models import *

router = APIRouter()


def authenticate_user(username: str, password: str):
    with db_interact.SQLiteContext() as db:
        # Check if username exists
        result = db.execute(
            "SELECT * FROM Users WHERE Username = ?",
            (username,),
        ).fetchone()

        if not result:
            return False

        # Check password
        if not bcrypt.checkpw(
            password.encode("utf-8"),
            result["HashedPassword"].encode("utf-8"),
        ):
            return False

        # Check if the user account is active
        if not result["IsUserActive"]:
            return False

        return result["HashedPassword"]


def create_access_token(data: dict):
    to_encode = data.copy()
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    with db_interact.SQLiteContext() as db:
        db.execute(
            "UPDATE Users SET UserToken = ? WHERE Username = ?",
            (encoded_jwt, data["sub"]),
        )
        return encoded_jwt


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user})

    # Save the token into the database
    with db_interact.SQLiteContext() as db:
        db.execute(
            "UPDATE Users SET UserToken = ? WHERE Username = ?",
            (access_token, form_data.username),
        )

    return {"access_token": access_token, "token_type": "bearer"}


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")
