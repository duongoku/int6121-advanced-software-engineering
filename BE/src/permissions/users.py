from fastapi_contrib.permissions import BasePermission
from dependencies import db_interact


class AuthenticatedPermission(BasePermission):
    def has_permission(self, request) -> bool:
        # Get the user id from the token in the Authorization header
        user_id = request.headers["Authorization"]
        # Get the user from the database
        with db_interact.SQLiteContext() as db:
            user = db.execute(
                "SELECT * FROM Users WHERE UserToken = ?",
                (user_id,),
            ).fetchone()

            # Check if the user is an admin
            if user:
                return True

        return False
