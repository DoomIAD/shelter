from database.database import get_db

# Returns all of the animals' info
def get_all_animals():
    db = get_db()

    animals = db.execute("""
        SELECT *
        FROM Animals
        ORDER BY name ASC
    """).fetchall()

    return [dict(animal) for animal in animals]

# Returns information of a single animal based on animal_id
def get_single_animal(animal_id):
    db = get_db()

    animal = db.execute("""
        SELECT *
        FROM Animals
        WHERE animal_id = ?
    """, (animal_id,)).fetchone()

    return dict(animal) if animal else None