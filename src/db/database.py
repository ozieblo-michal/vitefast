from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# URL bazy danych - tutaj używamy SQLite i zapisujemy bazę danych w pliku demodb.db.
SQLALCHEMY_DATABASE_URL = "sqlite:///./demodb.db"

# Tworzenie silnika SQLAlchemy, który będzie używany do interakcji z bazą danych.
# Parametr `connect_args` jest specyficzny dla SQLite w celu umożliwienia dostępu z wielu wątków.
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# Tworzenie fabryki sesji SQLAlchemy. Sesje są używane do zarządzania operacjami na bazie danych.
# `autocommit=False` oznacza, że SQLAlchemy nie zatwierdzi transakcji automatycznie.
# `autoflush=False` oznacza, że SQLAlchemy nie będzie automatycznie wysyłać zmian do bazy danych
# przy każdym zapytaniu.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Tworzenie klasy bazowej dla modeli danych.
# Klasy dziedziczące po `Base` będą mapowane na tabelę w bazie danych.
Base = declarative_base()
