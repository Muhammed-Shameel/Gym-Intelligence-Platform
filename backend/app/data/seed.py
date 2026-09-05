from sqlalchemy import inspect
from sqlalchemy.orm import Session
from app.models.domain import Member
from app.data.importer import import_csv_data

def seed_data(db: Session):
    # Check if data already exists to avoid duplicate constraint errors
    if db.query(Member).count() > 0:
        print("Database already seeded. Skipping.")
        return

    try:
        import_csv_data(db)
        print("Database seeded successfully with CSV data.")
    except Exception as e:
        print(f"Error seeding data: {e}")
        db.rollback()
