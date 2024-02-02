from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from route.route_limiter import limiter

import auth.auth as auth
import service.services as dummy_service
from db.dependencies import get_db
from schema.schemas import Dummy, DummyPatch, User

router = APIRouter()


@router.get("")
@router.get("/")
@limiter.limit("5/minute")
def read_root(request: Request, db: Session = Depends(get_db)):
    """Retrieve all dummy objects from the database.

    This endpoint queries the database and returns a list of all 'Dummy' objects.

    Args:
        db (Session, optional): A SQLAlchemy session dependency. Defaults to Depends(get_db).

    Returns:
        List[Dummy]: A list of 'Dummy' objects retrieved from the database.
    """
    return dummy_service.get_all(db)


@router.get("/{dummy_id}", response_model=Dummy)
@limiter.limit("5/minute")
def read_dummy(request: Request, dummy_id: int, db: Session = Depends(get_db)):
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
@limiter.limit("5/minute")
def create_dummy(
    request: Request,
    dummy: Dummy,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth.get_current_active_user),
):
    return dummy_service.create(dummy, db)


# TODO: add unit tests
@router.put("/{dummy_id}", response_model=Dummy)
@limiter.limit("5/minute")
def modify_completely(
    request: Request,
    dummy_id: int,
    dummy: Dummy,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth.get_current_active_user),
):
    return dummy_service.modify_completely(dummy_id, dummy, db)


@router.patch("/{dummy_id}", response_model=DummyPatch)
@limiter.limit("5/minute")
def modify_partially(
    request: Request,
    dummy_id: int,
    dummy: DummyPatch,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth.get_current_active_user),
):
    return dummy_service.modify_partially(dummy_id, dummy, db)


@router.delete("/{dummy_id}", status_code=204)
@limiter.limit("5/minute")
def delete_dummy(
    request: Request,
    dummy_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth.get_current_active_user),
):
    dummy_service.delete(dummy_id, db)
    return {"message": "Dummy object deleted successfully"}
