"""
Initialize the database with required tables and seed initial resource data.

This module contains logic to create database schema if it does not already
exist and seed the database with predefined resource data.
"""

from sqlalchemy.orm import Session

from.database import Base, SessionLocal, engine
from.models import Resource
from.seed_resources import resources


def init_db() -> None:
    Base.metadata.create_all(bind=engine)

    db: Session = SessionLocal()
    try:
        already_exists = db.query(Resource).first()
        if already_exists:
            return

        db.add_all(Resource(**resource) for resource in resources)
        db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    init_db()
