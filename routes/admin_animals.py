import os
import uuid

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    current_app
)

from werkzeug.utils import secure_filename
from database.database import get_db
from utils.decorators import admin_required

admin_animals = Blueprint(
    "admin_animals",
    __name__,
    url_prefix="/admin/animals"
)

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}

def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )

@admin_animals.route("/")
@admin_required
def index():
    conn = get_db()

    try:
        animals = conn.execute(
            """
            SELECT *
            FROM Animals
            ORDER BY name ASC
            """
        ).fetchall()

    finally:
        conn.close()

    return render_template(
        "admin/animals.html",
        animals=animals
    )

@admin_animals.route("/add", methods=["GET", "POST"])
@admin_required
def add():
    if request.method == "POST":
        animal_type = request.form.get("type", "").strip()
        name = request.form.get("name", "").strip()
        breed = request.form.get("breed", "").strip()
        age_months = request.form.get("age_months", "").strip()
        size = request.form.get("size", "").strip()
        sex = request.form.get("sex", "").strip()
        description = request.form.get("description", "").strip()

        # Check required fields
        if not all([
            animal_type, name, breed, age_months,
            size, sex, description
        ]):
            flash("Please fill out all required fields.")
            return render_template("admin/add_animal.html")

        # Validate age
        try:
            age_months = int(age_months)
            if age_months < 0:
                raise ValueError
        except ValueError:
            flash("Age must be a valid number of months.")
            return render_template("admin/add_animal.html")

        image = request.files.get("image")

        # Validate image before inserting the animal
        if image and image.filename:
            if not allowed_file(image.filename):
                flash("Please upload a PNG, JPG, JPEG, GIF, or WEBP image.")
                return render_template("admin/add_animal.html")

        conn = get_db()
        saved_image_path = None

        try:
            # Insert animal first so SQLite generates its ID
            cursor = conn.execute(
                """
                INSERT INTO Animals (
                    type,
                    name,
                    breed,
                    age_months,
                    size,
                    sex,
                    description
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    animal_type,
                    name,
                    breed,
                    age_months,
                    size,
                    sex,
                    description
                )
            )

            animal_id = cursor.lastrowid

            # Save image using the animal ID as its filename
            if image and image.filename:
                safe_filename = secure_filename(image.filename)
                extension = safe_filename.rsplit(".", 1)[1].lower()

                filename = f"{animal_id}.{extension}"

                upload_folder = os.path.join(
                    current_app.static_folder,
                    "uploads",
                    "animals"
                )

                os.makedirs(upload_folder, exist_ok=True)

                saved_image_path = os.path.join(upload_folder, filename)
                image.save(saved_image_path)

                image_path = f"uploads/animals/{filename}"

                # Update the animal with its image path
                conn.execute(
                    """
                    UPDATE Animals
                    SET image_path = ?
                    WHERE animal_id = ?
                    """,
                    (extension, animal_id)
                )

            conn.commit()

        except Exception:
            conn.rollback()

            if saved_image_path and os.path.exists(saved_image_path):
                os.remove(saved_image_path)

            raise

        finally:
            conn.close()

        flash(f"{name} was successfully added.")
        return redirect(url_for("admin_animals.index"))

    return render_template("admin/add_animal.html")