from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import auth.auth as auth
import service.services as dummy_service
from db.database import SessionLocal
from schema.schemas import Dummy, DummyPatch, User

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


@router.get("/{dummy_id}", response_model=Dummy)
def read_dummy(dummy_id: int, db: Session = Depends(get_db)):
    """Retrieve a dummy object from the database.

    This endpoint queries the database and returns the 'Dummy' object with the given ID.

    Args:
        dummy_id (int): The ID of the dummy object to be retrieved.
        db (Session, optional): A SQLAlchemy session dependency. Defaults to Depends(get_db).

    Returns:
        Dummy: The 'Dummy' object retrieved from the database.
    """
    return dummy_service.get_one(db, dummy_id)


@router.post("", status_code=201, response_model=Dummy)
@router.post("/", status_code=201, response_model=Dummy)
def create_dummy(
    dummy: Dummy,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth.get_current_active_user),
):
    return dummy_service.create(dummy, db)


@router.put("/{dummy_id}", response_model=Dummy)
def modify_completely(
    dummy_id: int,
    dummy: Dummy,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth.get_current_active_user),
):
    return dummy_service.modify_completely(dummy_id, dummy, db)


@router.patch("/{dummy_id}", response_model=DummyPatch)
def modify_partially(
    dummy_id: int,
    dummy: DummyPatch,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth.get_current_active_user),
):
    return dummy_service.modify_partially(dummy_id, dummy, db)


@router.delete("/{dummy_id}", status_code=204)
def delete_dummy(
    dummy_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth.get_current_active_user),
):
    dummy_service.delete(dummy_id, db)
    return {"message": "Dummy object deleted successfully"}
