from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
import model.models as models

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./demodb.db")


if SQLALCHEMY_DATABASE_URL:
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False}
        if "sqlite" in SQLALCHEMY_DATABASE_URL
        else {},
    )
else:
    raise ValueError("SQLALCHEMY_DATABASE_URL")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

models.Base.metadata.create_all(bind=engine)
