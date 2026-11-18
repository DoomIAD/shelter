from flask import Flask, render_template, request, redirect, url_for, session, flash
from database.database import get_db, init_db
from settings import SECRET_KEY
from werkzeug.security import generate_password_hash, check_password_hash
from routes.auth import auth
from utils.auth_helpers import get_current_user
from utils.decorators import admin_required

# DB getters/setters
from database.animals_access import get_animals
from database.autofill_db import autofill_animals

# Initialize Flask application
app = Flask(__name__)
app.secret_key = SECRET_KEY
app.register_blueprint(auth)
init_db()
autofill_animals()

@app.context_processor
def inject_user():
    return {"current_user": get_current_user()}

# Home
@app.route("/")
def home():
    animals = get_animals()
    return render_template("home.html", animals=animals)

@app.route("/admin")
@admin_required
def admin_dashboard():
    return "<h1>Admin Dashboard</h1><p>Access granted.</p>"

# Run the Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)