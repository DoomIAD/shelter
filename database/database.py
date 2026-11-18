import sqlite3
from getpass import getpass
from werkzeug.security import generate_password_hash

DATABASE = "shelter.db"


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def create_default_admin(conn):
    # Get the admin role ID
    admin_role = conn.execute(
        "SELECT role_id FROM Roles WHERE name = ?",
        ("admin",)
    ).fetchone()

    if admin_role is None:
        raise RuntimeError("Admin role does not exist.")

    # Check whether an admin account already exists
    existing_admin = conn.execute(
        "SELECT user_id FROM Users WHERE role_id = ? LIMIT 1",
        (admin_role["role_id"],)
    ).fetchone()

    if existing_admin:
        print("Admin account already exists.")
        return

    print("\nNo admin account found. Create the default administrator.")

    # Collect account information
    while True:
        first_name = input("First name: ").strip()
        last_name = input("Last name: ").strip()
        email = input("Email: ").strip().lower()

        if not first_name or not last_name or not email:
            print("First name, last name, and email are required.\n")
            continue

        # Check whether the email is already registered
        existing_user = conn.execute(
            "SELECT user_id FROM Users WHERE email = ?",
            (email,)
        ).fetchone()

        if existing_user:
            print("That email is already registered. Try another email.\n")
            continue

        password = getpass("Password: ")
        confirm_password = getpass("Confirm password: ")

        if len(password) < 8:
            print("Password must be at least 8 characters long.\n")
            continue

        if password != confirm_password:
            print("Passwords do not match. Try again.\n")
            continue

        break

    # Hash the password
    password_hash = generate_password_hash(password)

    # Insert the administrator account
    conn.execute(
        """
        INSERT INTO Users (
            role_id, first_name, last_name, email, password_hash
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            admin_role["role_id"],
            first_name,
            last_name,
            email,
            password_hash
        )
    )

    print(f"\nAdministrator account created for {email}.\n")

def init_db():
    with get_db() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS Roles (
                role_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE
            );

            CREATE TABLE IF NOT EXISTS Users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                role_id INTEGER NOT NULL,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                phone TEXT,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (role_id) REFERENCES Roles(role_id)
            );

            CREATE TABLE IF NOT EXISTS Sessions (
                session_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                token_hash TEXT NOT NULL UNIQUE,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                expires_at TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES Users(user_id)
            );

            CREATE TABLE IF NOT EXISTS Animals (
                animal_id INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT NOT NULL,
                name TEXT NOT NULL,
                breed TEXT NOT NULL,
                age_months INTEGER NOT NULL,
                size TEXT NOT NULL,
                sex TEXT NOT NULL,
                description TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'available',
                image_path TEXT
            );

            CREATE TABLE IF NOT EXISTS MedicalRecords (
                record_id INTEGER PRIMARY KEY AUTOINCREMENT,
                animal_id INTEGER NOT NULL UNIQUE,
                vaccinations TEXT NOT NULL,
                is_spayed_neutered INTEGER NOT NULL DEFAULT 0,
                dietary_needs TEXT NOT NULL,
                behavior TEXT NOT NULL,
                special_care TEXT,
                FOREIGN KEY (animal_id) REFERENCES Animals(animal_id)
            );

            CREATE TABLE IF NOT EXISTS Favorites (
                user_id INTEGER NOT NULL,
                animal_id INTEGER NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (user_id, animal_id),
                FOREIGN KEY (user_id) REFERENCES Users(user_id),
                FOREIGN KEY (animal_id) REFERENCES Animals(animal_id)
            );

            CREATE TABLE IF NOT EXISTS AdoptionApplications (
                adopt_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                animal_id INTEGER NOT NULL,
                address_line TEXT NOT NULL,
                city TEXT NOT NULL,
                state TEXT NOT NULL,
                zip_code TEXT NOT NULL,
                phone TEXT NOT NULL,
                living_situation TEXT NOT NULL,
                pet_experience TEXT NOT NULL,
                additional_info TEXT,
                status TEXT NOT NULL DEFAULT 'pending',
                submitted_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                reviewed_by INTEGER,
                reviewed_at TEXT,
                notes TEXT,
                FOREIGN KEY (user_id) REFERENCES Users(user_id),
                FOREIGN KEY (animal_id) REFERENCES Animals(animal_id),
                FOREIGN KEY (reviewed_by) REFERENCES Users(user_id)
            );

            CREATE TABLE IF NOT EXISTS VolunteerOpportunities (
                opportunity_id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS VolunteerShifts (
                shift_id INTEGER PRIMARY KEY AUTOINCREMENT,
                opportunity_id INTEGER NOT NULL,
                shift_date TEXT NOT NULL,
                time_start TEXT NOT NULL,
                time_end TEXT NOT NULL,
                capacity INTEGER NOT NULL DEFAULT 1,
                FOREIGN KEY (opportunity_id)
                    REFERENCES VolunteerOpportunities(opportunity_id)
            );

            CREATE TABLE IF NOT EXISTS VolunteerApplications (
                volunteer_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                shift_id INTEGER NOT NULL,
                application_info TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'pending',
                submitted_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                reviewed_by INTEGER,
                reviewed_at TEXT,
                notes TEXT,
                FOREIGN KEY (user_id) REFERENCES Users(user_id),
                FOREIGN KEY (shift_id) REFERENCES VolunteerShifts(shift_id),
                FOREIGN KEY (reviewed_by) REFERENCES Users(user_id)
            );
        """)
        conn.executemany(
            "INSERT OR IGNORE INTO Roles (name) VALUES (?)",
            [
                ("admin",),
                ("user",)
            ]
        )
        create_default_admin(conn)