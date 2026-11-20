from flask import Blueprint, render_template

from database.database import get_db
from utils.decorators import admin_required


admin_applications = Blueprint(
    "admin_applications",
    __name__,
    url_prefix="/admin"
)


@admin_applications.route("/adoptions")
@admin_required
def adoptions():
    conn = get_db()

    try:
        applications = conn.execute(
            """
            SELECT
                AdoptionApplications.*,
                Users.first_name,
                Users.last_name,
                Users.email,
                Animals.name AS animal_name
            FROM AdoptionApplications
            JOIN Users
                ON AdoptionApplications.user_id = Users.user_id
            JOIN Animals
                ON AdoptionApplications.animal_id = Animals.animal_id
            ORDER BY AdoptionApplications.submitted_at DESC
            """
        ).fetchall()

    finally:
        conn.close()

    return render_template(
        "admin/adoptions.html",
        applications=applications
    )


@admin_applications.route("/volunteering")
@admin_required
def volunteering():
    conn = get_db()

    try:
        applications = conn.execute(
            """
            SELECT
                VolunteerApplications.*,
                Users.first_name,
                Users.last_name,
                Users.email,
                VolunteerOpportunities.title AS opportunity_title,
                VolunteerShifts.shift_date,
                VolunteerShifts.time_start,
                VolunteerShifts.time_end
            FROM VolunteerApplications
            JOIN Users
                ON VolunteerApplications.user_id = Users.user_id
            JOIN VolunteerShifts
                ON VolunteerApplications.shift_id = VolunteerShifts.shift_id
            JOIN VolunteerOpportunities
                ON VolunteerShifts.opportunity_id =
                   VolunteerOpportunities.opportunity_id
            ORDER BY VolunteerApplications.submitted_at DESC
            """
        ).fetchall()

    finally:
        conn.close()

    return render_template(
        "admin/volunteering.html",
        applications=applications
    )