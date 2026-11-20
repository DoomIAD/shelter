from flask import Flask, render_template, request, redirect, url_for, session, flash
from database.database import get_db, init_db
from settings import SECRET_KEY
from werkzeug.security import generate_password_hash, check_password_hash
from routes.auth import auth
from utils.auth_helpers import get_current_user
from utils.decorators import admin_required
from routes.admin import admin
from routes.admin_animals import admin_animals

# DB getters/setters
from database.animals_access import get_all_animals, get_single_animal
from database.autofill_db import autofill_animals

# Initialize Flask application
app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024
app.secret_key = SECRET_KEY
app.register_blueprint(auth)
app.register_blueprint(admin)
app.register_blueprint(admin_animals)

init_db()
autofill_animals()

@app.context_processor
def inject_user():
    return {"current_user": get_current_user()}

# Home
@app.route("/")
def home():
    # Passes all of the animals saved to the DB
    animals = get_all_animals()
    return render_template("home.html", animals=animals)

# Animal Listing
@app.get('/animal_listing/<animal_id>')
def animal_listing(animal_id):
    # Passes the given animal's information based on their ID via URL
    animal=get_single_animal(animal_id)
    return render_template("animal_listing.html", animal=animal)

#===============================================================================
# Website Functions
@app.template_filter("age")
def age(months):
    if months >= 12:
        years = months // 12
        new_months = months % 12

        if years == 1:
            return f"{years} year"
        else:
            return f"{years} years"

    return f"{months} months"

# Run the Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)