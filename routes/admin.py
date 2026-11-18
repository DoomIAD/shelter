from flask import Blueprint, render_template
from utils.decorators import admin_required

admin = Blueprint("admin", __name__, url_prefix="/admin")


@admin.route("/")
@admin_required
def dashboard():
    return render_template("admin/dashboard.html")