from fastapi import HTTPException
from sqlalchemy.orm import Session

import model.models as models
import schema.schemas as schemas


from sqlalchemy.exc import NoResultFound


import logging

logger = logging.getLogger("configure_logger")


def generate_error():
    logger = logging.getLogger("configure_logger")
    logger.error("This is a test error message")
    raise HTTPException(status_code=500, detail="This is a test error")



def get_all(db: Session):
    sqlalchemy_model = db.query(models.Dummy).all()

    if not sqlalchemy_model:
        logger.error("404: Object not found")
        raise HTTPException(status_code=404, detail="Object not found")

    return sqlalchemy_model


def get_object_or_404(db: Session, model, **criteria):
    try:
        return db.query(model).filter_by(**criteria).one()
    except NoResultFound:
        logger.error("404: Object not found")
        raise HTTPException(status_code=404, detail="Object not found")


def create(dummy: schemas.Dummy, db: Session):
    existing_dummy = (
        db.query(models.Dummy).filter(models.Dummy.name == dummy.name).first()
    )
    if existing_dummy:
        logger.error("Duplicate")
        raise HTTPException(
            status_code=400,
            detail="Record including name '{}' already exists".format(dummy.name),
        )

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
    sqlalchemy_model = get_object_or_404(db, models.Dummy, id=dummy_id)

    for key, value in dummy.dict().items():
        setattr(sqlalchemy_model, key, value)

    db.commit()
    db.refresh(sqlalchemy_model)

    return sqlalchemy_model


def modify_partially(dummy_id: int, dummy: schemas.Dummy, db: Session):
    sqlalchemy_model = get_object_or_404(db, models.Dummy, id=dummy_id)

    update_data = dummy.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(sqlalchemy_model, key, value)

    db.commit()
    db.refresh(sqlalchemy_model)

    return sqlalchemy_model


def delete(dummy_id: int, db: Session):
    sqlalchemy_model = get_object_or_404(db, models.Dummy, id=dummy_id)

    db.delete(sqlalchemy_model)
    db.commit()

    return sqlalchemy_model


def get_one(db: Session, dummy_id: int):
    return get_object_or_404(db, models.Dummy, id=dummy_id)


def create_user(db: Session, user: schemas.UserInDB):
    existing_user = (
        db.query(models.User).filter(models.User.email == user.email).first()
    )
    if existing_user:
        logger.error("400: Email already exists")
        raise HTTPException(status_code=400, detail="Email already exists")

    db_user = models.User(
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        password=user.hashed_password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# TODO: put hashing here
