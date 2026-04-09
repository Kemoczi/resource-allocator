from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import inspect
from sqlalchemy.orm import Session

from . import models, schemas
from .database import SessionLocal

from time import sleep

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    db: Session = SessionLocal()
    try:
        if not inspect(db.bind).has_table("resources"):
            raise RuntimeError("Database is not initialized. Run init_db.py first.")
        yield
    finally:
        db.close()


app = FastAPI(lifespan=lifespan)


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
        request: schemas.AssignInterfaceRequest,
        db: Session = Depends(get_db)
):
    query = db.query(models.Resource).filter(models.Resource.assigned == False)

    if not any([request.location, request.phy_speed, request.optics]):
        raise HTTPException(status_code=400, detail="You must provide at least one resource parameter")

    if request.location is not None:
        query = query.filter(models.Resource.location == request.location)
    if request.phy_speed is not None:
        query = query.filter(models.Resource.phy_speed == request.phy_speed)
    if request.optics is not None:
        query = query.filter(models.Resource.optics == request.optics)

    resource = query.first()

    if not resource:
        raise HTTPException(status_code=404, detail="No resources with specified parameters available")

    resource.assigned = True
    db.commit()
    db.refresh(resource)
    return resource


@app.get("/resources/", response_model=list[schemas.Resource])
def read_resources(db: Session = Depends(get_db)):
    sleep(3)
    resources = db.query(models.Resource).all()
    return resources
