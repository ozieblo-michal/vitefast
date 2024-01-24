from fastapi import HTTPException
from sqlalchemy.orm import Session

import model.models as models
import schema.schemas as schemas

import logging
logger = logging.getLogger("configure_logger")


def get_all(db: Session):
    """Retrieve all records of 'Dummy' from the database.

    This function fetches all entries from the 'dummy' table using SQLAlchemy's ORM capabilities.

    Args:
        db (Session): The SQLAlchemy session facilitating database connectivity.

    Returns:
        List[models.Dummy]: A list of 'Dummy' model objects representing all records in the 'dummy' table.
    """
    sqlalchemy_model = db.query(models.Dummy).all()

    if not sqlalchemy_model:
        logger.error("404: Object not found")
        raise HTTPException(status_code=404, detail="Object not found")

    return sqlalchemy_model


def create(dummy: schemas.Dummy, db: Session):
    """Create a new 'Dummy' record in the database.

    This function takes a 'Dummy' schema object, maps it to the SQLAlchemy model, and stores it in the database.

    Args:
        db (Session): The SQLAlchemy session facilitating database connectivity.
        dummy (schemas.Dummy): The Pydantic schema object representing the data to be added to the database.

    Returns:
        models.Dummy: The newly created 'Dummy' model object, now stored in the database.
    """

    existing_dummy = (
        db.query(models.Dummy).filter(models.Dummy.name == dummy.name).first()
    )
    if existing_dummy:
        logger.error("Duplicate")
        raise ValueError(f"Record including name '{dummy.name}' already exists")

    # Mapping the Pydantic schema object to the SQLAlchemy model
    sqlalchemy_model = models.Dummy()
    sqlalchemy_model.name = dummy.name
    sqlalchemy_model.description = dummy.description
    sqlalchemy_model.optional_field = dummy.optional_field

    # Adding and committing the new record to the database
    db.add(sqlalchemy_model)
    db.commit()

    return sqlalchemy_model


def modify_completely(dummy_id: int, dummy: schemas.Dummy, db: Session):
    sqlalchemy_model = (
        db.query(models.Dummy).filter(models.Dummy.id == dummy_id).first()
    )

    if not sqlalchemy_model:
        logger.error("404: Object not found")
        raise HTTPException(status_code=404, detail="Object not found")

    sqlalchemy_model.name = dummy.name
    sqlalchemy_model.description = dummy.description
    sqlalchemy_model.optional_field = dummy.optional_field

    db.add(sqlalchemy_model)
    db.commit()

    return sqlalchemy_model


def modify_partially(dummy_id: int, dummy: schemas.Dummy, db: Session):
    sqlalchemy_model = (
        db.query(models.Dummy).filter(models.Dummy.id == dummy_id).first()
    )

    if not sqlalchemy_model:
        # logger.error("404: Object not found")
        raise HTTPException(status_code=404, detail="Object not found")

    update_data = dummy.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(sqlalchemy_model, key, value)

    # db.add(sqlalchemy_model)
    db.commit()

    return sqlalchemy_model


def delete(dummy_id: int, db: Session):
    sqlalchemy_model = (
        db.query(models.Dummy).filter(models.Dummy.id == dummy_id).first()
    )

    if not sqlalchemy_model:
        logger.error("404: Object not found")
        raise HTTPException(status_code=404, detail="Object not found")

    db.delete(sqlalchemy_model)
    db.commit()

    return sqlalchemy_model


def get_one(db: Session, dummy_id: int):
    sqlalchemy_model = (
        db.query(models.Dummy).filter(models.Dummy.id == dummy_id).first()
    )

    if not sqlalchemy_model:
        logger.error("404: Object not found")
        raise HTTPException(status_code=404, detail="Object not found")

    return sqlalchemy_model





def create_user(db: Session, user: schemas.User):
    db_user = models.User(username=user.username, 
                          email=user.email, 
                          full_name=user.full_name,
                          hashed_password=user.hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# TODO: put hashing here