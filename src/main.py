from fastapi import FastAPI, Depends
from pydantic import BaseModel, Field
import model.models as models
from db.database import engine, SessionLocal
from sqlalchemy.orm import Session
import uvicorn

# Utworzenie instancji FastAPI.
app = FastAPI()

# Inicjalizacja tabel w bazie danych na podstawie modeli z SQLAlchemy.
models.Base.metadata.create_all(bind=engine)


# Funkcja zależności do uzyskania sesji bazy danych.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Model Pydantic, używany do walidacji danych wejściowych dla żądań.
class Dummy(BaseModel):
    # Pole `id` typu UUID jest zakomentowane, aby uniknąć konfliktu z modelem SQLAlchemy.
    # id: UUID
    name: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1, max_length=100)


# Endpoint GET, który zwraca wszystkie obiekty Dummy z bazy danych.
@app.get("/")
def read_root(db: Session = Depends(get_db)):
    return db.query(models.Dummy).all()


# Endpoint POST, który tworzy nowy obiekt Dummy w bazie danych.
@app.post("/")
def create_dummy(dummy: Dummy, db: Session = Depends(get_db)):
    dummy_model = models.Dummy()
    dummy_model.name = dummy.name
    dummy_model.description = dummy.description
    db.add(dummy_model)
    db.commit()
    return dummy_model


# Uruchomienie serwera Uvicorn, jeśli plik jest uruchamiany jako główny program.
if __name__ == "__main__":
    # Argument `reload=True` pozwala na automatyczne przeładowanie serwera przy zmianie kodu.
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
    # Można również uruchomić serwer z wieloma workerami, ale bez opcji przeładowania.
    # uvicorn.run("main:app", host="127.0.0.1", port=8000, workers=2)
