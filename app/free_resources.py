from sqlalchemy.orm import Session

from.database import SessionLocal
from.models import Resource

def free_resources() -> None:

    db: Session = SessionLocal()

    try:
        db.query(Resource).filter(Resource.assigned == True).update(
            {Resource.assigned: False}
        )
        db.commit()
    except:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    free_resources()
