from flask import Blueprint, render_template

from database.database import get_db
from utils.decorators import admin_required


admin_users = Blueprint(
    "admin_users",
    __name__,
    url_prefix="/admin/users"
)


@admin_users.route("/")
@admin_required
def index():
    conn = get_db()

    try:
        users = conn.execute(
            """
            SELECT
                Users.user_id,
                Users.first_name,
                Users.last_name,
                Users.email,
                Users.phone,
                Users.created_at,
                Roles.name AS role
            FROM Users
            JOIN Roles
                ON Users.role_id = Roles.role_id
            ORDER BY Users.last_name, Users.first_name
            """
        ).fetchall()

    finally:
        conn.close()

    return render_template(
        "admin/users.html",
        users=users
    )