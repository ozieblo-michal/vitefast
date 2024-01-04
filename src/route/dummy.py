from fastapi import Depends, APIRouter
import model.models as models
from db.database import engine, SessionLocal
from sqlalchemy.orm import Session
from schema.schemas import Dummy

router = APIRouter()

# Inicjalizacja tabel w bazie danych na podstawie modeli z SQLAlchemy.
models.Base.metadata.create_all(bind=engine)


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
    return db.query(models.Dummy).all()


# Endpoint POST, który tworzy nowy obiekt Dummy w bazie danych.
@router.post("", status_code=201, response_model=Dummy)
@router.post("/", status_code=201, response_model=Dummy)
def create_dummy(dummy: Dummy, db: Session = Depends(get_db)):
    dummy_model = models.Dummy()
    dummy_model.name = dummy.name
    dummy_model.description = dummy.description
    db.add(dummy_model)
    db.commit()
    return dummy_model


