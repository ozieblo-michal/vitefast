from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import service.dummy as dummy_service
from db.database import SessionLocal
from schema.schemas import Dummy

router = APIRouter()

def get_db():
    """Dependency function to obtain a database session.

    This function yields a SQLAlchemy session from a session factory upon request and closes it after use.

    Yields:
        Session: A SQLAlchemy session object to interact with the database.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("")
@router.get("/")
def read_root(db: Session = Depends(get_db)):
    """Retrieve all dummy objects from the database.

    This endpoint queries the database and returns a list of all 'Dummy' objects.

    Args:
        db (Session, optional): A SQLAlchemy session dependency. Defaults to Depends(get_db).

    Returns:
        List[Dummy]: A list of 'Dummy' objects retrieved from the database.
    """
    return dummy_service.get_all(db)

@router.post("", status_code=201, response_model=Dummy)
@router.post("/", status_code=201, response_model=Dummy)
def create_dummy(dummy: Dummy, db: Session = Depends(get_db)):
    """Create a new dummy object in the database.

    This endpoint takes a 'Dummy' schema object and adds it to the database.

    Args:
        dummy (Dummy): A 'Dummy' schema object containing the data to be added.
        db (Session, optional): A SQLAlchemy session dependency. Defaults to Depends(get_db).

    Returns:
        Dummy: The 'Dummy' object that was added to the database.
    """
    return dummy_service.create(db, dummy)
