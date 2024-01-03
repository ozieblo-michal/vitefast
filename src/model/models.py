from sqlalchemy import Column, Integer, String
from db.database import Base

# Definicja klasy modelu SQLAlchemy, reprezentującej tabelę w bazie danych.
class Dummy(Base):
    # Nazwa tabeli w bazie danych.
    __tablename__ = "dummy"

    # Definicja kolumn tabeli. Każda kolumna jest atrybutem klasy.

    # Kolumna 'id', która jest kluczem głównym tabeli. 
    # 'Integer' oznacza, że używamy typu danych liczbowych całkowitych.
    # 'primary_key=True' wskazuje, że to pole jest kluczem głównym.
    # 'index=True' oznacza utworzenie indeksu dla tej kolumny, co poprawia wydajność zapytań.
    id = Column(Integer, primary_key=True, index=True)

    # Kolumna 'name', przechowująca ciągi znaków (String).
    # Domyślnie nie jest to pole wymagane i może przyjąć wartości NULL.
    name = Column(String)

    # Kolumna 'description', także przechowująca ciągi znaków.
    # Podobnie jak 'name', domyślnie może przyjąć wartości NULL.
    description = Column(String)
