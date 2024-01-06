
from sqlalchemy.orm import Session
import schema.schemas as schemas
import model.models as models

import auth

def get_all(db: Session):
    return db.query(models.Dummy).all()

def create(db: Session, dummy: schemas.Dummy):
    sqlalchemy_model = models.Dummy()
    sqlalchemy_model.name = dummy.name
    sqlalchemy_model.description = dummy.description
    db.add(sqlalchemy_model)
    db.commit()
    return sqlalchemy_model