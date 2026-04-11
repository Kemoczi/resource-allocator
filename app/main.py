from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session

from . import models, schemas
from .database import SessionLocal

app = FastAPI()


def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    except OperationalError as exc:
        print("\nERROR - Database is not initialized. Run python -m app.init_db\n")
        raise HTTPException(
            status_code=500,
            detail="ERROR - Database is not initialized. Run python -m app.init_db"
        ) from exc
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"message": "Hello, this is resource allocator! ;)"}


@app.post("/resources/assign-interface", response_model=schemas.Resource)
def assign_interface(
        request: schemas.AssignInterfaceRequest,
        db: Session = Depends(get_db)
):
    query = db.query(models.Resource).filter(models.Resource.assigned == False)

    if not any([request.location, request.phy_speed, request.optics]):
        raise HTTPException(
            status_code=400, detail="You must provide at least one resource parameter"
        )

    if request.location is not None:
        query = query.filter(models.Resource.location == request.location)
    if request.phy_speed is not None:
        query = query.filter(models.Resource.phy_speed == request.phy_speed)
    if request.optics is not None:
        query = query.filter(models.Resource.optics == request.optics)

    resource = query.first()

    if not resource:
        raise HTTPException(
            status_code=404, detail="No resources with specified parameters available"
        )

    resource.assigned = True
    db.commit()
    db.refresh(resource)
    return resource


@app.get("/resources/", response_model=list[schemas.Resource])
def read_resources(db: Session = Depends(get_db)):
    resources = db.query(models.Resource).all()
    return resources
