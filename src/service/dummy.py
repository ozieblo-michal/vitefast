from sqlalchemy.orm import Session

import model.models as models
import schema.schemas as schemas

def get_all(db: Session):
    """Retrieve all records of 'Dummy' from the database.

    This function fetches all entries from the 'dummy' table using SQLAlchemy's ORM capabilities.

    Args:
        db (Session): The SQLAlchemy session facilitating database connectivity.

    Returns:
        List[models.Dummy]: A list of 'Dummy' model objects representing all records in the 'dummy' table.
    """
    return db.query(models.Dummy).all()


def create(db: Session, dummy: schemas.Dummy):
    """Create a new 'Dummy' record in the database.

    This function takes a 'Dummy' schema object, maps it to the SQLAlchemy model, and stores it in the database.

    Args:
        db (Session): The SQLAlchemy session facilitating database connectivity.
        dummy (schemas.Dummy): The Pydantic schema object representing the data to be added to the database.

    Returns:
        models.Dummy: The newly created 'Dummy' model object, now stored in the database.
    """
    # Mapping the Pydantic schema object to the SQLAlchemy model
    sqlalchemy_model = models.Dummy()
    sqlalchemy_model.name = dummy.name
    sqlalchemy_model.description = dummy.description

    # Adding and committing the new record to the database
    db.add(sqlalchemy_model)
    db.commit()

    return sqlalchemy_model
