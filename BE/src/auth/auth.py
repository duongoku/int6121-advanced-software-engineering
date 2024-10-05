from fastapi import APIRouter, Depends, HTTPException

from dependencies import db_interact
from user_management import authentication

router = APIRouter()


@router.get("/check_token")
def get_my_organizations(token: str = Depends(authentication.oauth2_scheme)):
    """
    Check if the given token is valid and returns a message if it is.
    """
    with db_interact.SQLiteContext() as db:
        # get the user id from the token
        user = db.execute(
            "SELECT * FROM Users WHERE UserToken = ?",
            (token,),
        ).fetchone()

        if not user:
            raise HTTPException(status_code=403, detail="Unauthorized")

        return {"message": "Authorized"}
