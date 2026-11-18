from database.database import get_db

def autofill_animals():
    db = get_db()

    animals = [
        (
            1001, "Dog", "Biscuit", "Labrador Retriever",
            27, "Large", "Male",
            "Friendly Labrador Retriever looking for a loving home.",
            "available"
        ),
        (
            1002, "Cat", "Luna", "Domestic Shorthair",
            7, "Small", "Female",
            "Sweet Domestic Shorthair looking for a loving home.",
            "available"
        ),
        (
            1003, "Dog", "Pepper", "Beagle",
            80, "Medium", "Female",
            "Beagle who has already found a home.",
            "adopted"
        ),
        (
            1004, "Rabbit", "Clover", "Holland Lop",
            24, "Small", "Female",
            "Holland Lop currently pending adoption.",
            "pending"
        )
    ]

    db.executemany("""
        INSERT OR IGNORE INTO Animals (
            animal_id,
            type,
            name,
            breed,
            age_months,
            size,
            sex,
            description,
            status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, animals)

    db.commit()
