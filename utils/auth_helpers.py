from flask import session
from database.database import get_db

def get_current_user():
    user_id = session.get("user_id")

    if user_id is None:
        return None

    conn = get_db()
    try:
        user = conn.execute(
            """
            SELECT Users.user_id, Users.first_name, Users.last_name,
                   Users.email, Roles.name AS role
            FROM Users
            JOIN Roles ON Users.role_id = Roles.role_id
            WHERE Users.user_id = ?
            """,
            (user_id,)
        ).fetchone()

        return user
    finally:
        conn.close()

