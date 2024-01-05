from fastapi import Depends, APIRouter
from db.database import SessionLocal
from sqlalchemy.orm import Session
from schema.schemas import Dummy

import service.dummy as dummy_service

router = APIRouter()




# Funkcja zależności do uzyskania sesji bazy danych.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# user = db.query(User).first()  # Pobranie użytkownika z bazy danych SQLAlchemy
# user_schema = UserInDB.from_orm(user)  # Konwersja na model Pydantic


# Endpoint GET, który zwraca wszystkie obiekty Dummy z bazy danych.
@router.get("")
@router.get("/")
def read_root(db: Session = Depends(get_db)):
    return dummy_service.get_all(db)


# Endpoint POST, który tworzy nowy obiekt Dummy w bazie danych.
@router.post("", status_code=201, response_model=Dummy)
@router.post("/", status_code=201, response_model=Dummy)
def create_dummy(dummy: Dummy, db: Session = Depends(get_db)):
    return dummy_service.create(db, dummy)


