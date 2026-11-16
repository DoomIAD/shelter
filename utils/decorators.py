from functools import wraps
from flask import flash, redirect, url_for
from utils.auth_helpers import get_current_user

def admin_required(route_function):
    @wraps(route_function)
    def decorated_function(*args, **kwargs):
        user = get_current_user()

        if user is None:
            flash("Please log in to access this page.")
            return redirect(url_for("login"))

        if user["role"] != "admin":
            flash("You do not have permission to access this page.")
            return redirect(url_for("home"))

        return route_function(*args, **kwargs)

    return decorated_function