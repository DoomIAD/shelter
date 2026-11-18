from database.database import get_db

# Returns all of the animal's info
def get_animals():
    db = get_db()

    animals = db.execute("""
        SELECT *
        FROM Animals
        ORDER BY name ASC
    """).fetchall()

    return [dict(animal) for animal in animals]