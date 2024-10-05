from pydantic import BaseModel
from typing import Optional
from dependencies import db_interact

# CREATE TABLE IF NOT EXISTS "Users" (
# 	"UUID"	TEXT NOT NULL UNIQUE,
# 	"Username"	TEXT NOT NULL UNIQUE,
# 	"HashedPassword"	BLOB NOT NULL,
# 	"IsUserActive"	INTEGER DEFAULT 1,
# 	"IsProfileVisible"	INTEGER DEFAULT 1,
# 	"PermissionMask"	INTEGER DEFAULT 0,
# 	"UserToken"	TEXT,
# 	PRIMARY KEY("UUID")
# );


class User(BaseModel):
    UUID: str
    Username: str
    HashedPassword: str
    IsUserActive: bool
    IsProfileVisible: bool
    PermissionMask: int
    UserToken: Optional[str]


class UserInDB(User):
    hashed_password: str
    token: str = None

    @staticmethod
    def get_user_by_token(token: str) -> str:
        db = db_interact.get_db()
        result = db.execute(
            "SELECT * FROM Users WHERE token = ?",
            (token,),
        ).fetchone()
        if not result:
            return None
        return UserInDB(**result)


class Token(BaseModel):
    access_token: str

    def get_user(self) -> str:
        db = db_interact.get_db()
        result = db.execute(
            "SELECT * FROM Users WHERE token = ?",
            (self.access_token,),
        ).fetchone()
        if not result:
            return None
        return result["UUID"]
