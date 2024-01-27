from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
import model.models as models

if os.getenv("RUNNING_IN_CONTAINER") == "yes":
    SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@db:5432/mydatabase")
else:
    SQLALCHEMY_DATABASE_URL = "sqlite:///./demodb.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False} if 'sqlite' in SQLALCHEMY_DATABASE_URL else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

models.Base.metadata.create_all(bind=engine)
