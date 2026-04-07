from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, HTTPException

from . import models, schemas
from.database import engine, SessionLocal, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Hello, this is resource allocator! ;)"}


@app.post("/resources/assign-interface", response_model=schemas.Resource)
def assign_interface(
        location: str | None = None,
        phy_speed: str | None = None,
        optics: str | None = None,
        db: Session = Depends(get_db)
):
    query = db.query(models.Resource).filter(models.Resource.assigned == False)

    if not any([location, phy_speed, optics]):
        raise HTTPException(status_code=400, detail="You must provide at least one resource parameter")

    if location is not None:
        query = query.filter(models.Resource.location == location)
    if phy_speed is not None:
        query = query.filter(models.Resource.phy_speed == phy_speed)
    if optics is not None:
        query = query.filter(models.Resource.optics == optics)

    resource = query.first()

    if not resource:
        raise HTTPException(status_code=404, detail="No resources with specified parameters available")

    resource.assigned = True
    db.commit()
    db.refresh(resource)
    return resource


@app.get("/resources/", response_model=list[schemas.Resource])
def read_resources(db: Session = Depends(get_db)):
    resources = db.query(models.Resource).all()
    return resources
