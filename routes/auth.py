from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from database.database import get_db
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint("auth", __name__)

# Login
@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        conn = get_db()
        try:
            user = conn.execute(
                "SELECT * FROM Users WHERE email = ?",
                (email,)
            ).fetchone()

            # Verify the account and password
            if user is None or not check_password_hash(
                user["password_hash"], password
            ):
                flash("Invalid email or password.")
                return render_template("login.html")

            # Store the user's ID in the session
            session.clear()
            session["user_id"] = user["user_id"]

            flash("You have successfully logged in.")
            return redirect(url_for("home"))

        finally:
            conn.close()

    return render_template("login.html")

# Logout
@auth.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.")
    return redirect(url_for("home"))

# Registration
@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        first_name = request.form.get("first_name", "").strip()
        last_name = request.form.get("last_name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        phone = request.form.get("phone", "").strip()

        if not first_name or not last_name or not email or len(password) < 8:
            flash("Please complete all required fields. Passwords must be at least 8 characters.")
            return render_template("register.html")

        # Check whether the email is already registered
        conn = get_db()
        try:
            existing_user = conn.execute(
                "SELECT user_id FROM Users WHERE email = ?",
                (email,)
            ).fetchone()

            if existing_user:
                flash("An account with that email already exists.")
                return render_template("register.html")

            # Find the regular user role
            role = conn.execute(
                "SELECT role_id FROM Roles WHERE name = ?",
                ("user",)
            ).fetchone()

            if role is None:
                flash("Registration is currently unavailable.")
                return render_template("register.html")

            # Hash the password before storing it
            password_hash = generate_password_hash(password)

            # Create the user account
            cursor = conn.execute(
                """
                INSERT INTO Users (
                    role_id, first_name, last_name, email,
                    password_hash, phone
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    role["role_id"],
                    first_name,
                    last_name,
                    email,
                    password_hash,
                    phone or None
                )
            )

            conn.commit()

            # Log the new user in
            session.clear()
            session["user_id"] = cursor.lastrowid

            flash("Your account was created successfully.")
            return redirect(url_for("home"))

        finally:
            conn.close()

    return render_template("register.html")