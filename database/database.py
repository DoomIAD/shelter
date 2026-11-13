import sqlite3

DATABASE = "shelter.db"


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


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
                status TEXT NOT NULL DEFAULT 'available'
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