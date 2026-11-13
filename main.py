from flask import Flask, render_template, request, redirect, url_for, session, flash
from database.database import get_db, init_db
from secrets import SECRET_KEY

# Initialize Flask application
app = Flask(__name__)
app.secret_key = SECRET_KEY
init_db()

# Home
@app.route("/")
def home():
    return render_template("home.html")

# Login
@app.route("/login")
def login():
    return render_template("login.html")

# Run the Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)