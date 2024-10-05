from fastapi_contrib.permissions import BasePermission
from dependencies import db_interact


class AdminPermission(BasePermission):
    def has_required_permissions(self, request) -> bool:
        # If the request is not authenticated, return False
        if not request.headers.get("Authorization"):
            return False
        # Get the user id from the token in the Authorization header
        user_id = request.headers["Authorization"].split(" ")[1]
        # Get the user from the database
        with db_interact.SQLiteContext() as db:
            user = db.execute(
                "SELECT * FROM Users WHERE UserToken = ?",
                (user_id,),
            ).fetchone()

            if not user:
                return False

            # Check if the user is an admin
            if user["Permissions"] == "admin":
                return True

        return False
