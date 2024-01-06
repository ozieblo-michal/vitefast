from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import model.models as models

# Database URL - here we are using SQLite and storing the database in the file 'demodb.db'.
# SQLite is chosen for simplicity and ease of setup, as it does not require a separate database server.
SQLALCHEMY_DATABASE_URL = "sqlite:///./demodb.db"

# Creating a SQLAlchemy engine that will be used for interacting with the database.
# The `connect_args` parameter is specific to SQLite to allow access from multiple threads.
# This setup is necessary because, by default, SQLite only allows access from the thread that created the database connection.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Creating a session factory for SQLAlchemy. Sessions are used to manage database operations.
# `autocommit=False` means SQLAlchemy will not commit transactions automatically,
# giving more control over when to commit.
# `autoflush=False` means SQLAlchemy will not automatically flush changes to the database
# on every query, providing more control over when data is sent to the database.
# This setup is important for managing transactions and database state explicitly, 
# ensuring data integrity and consistency.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Initializing tables in the database based on models defined in SQLAlchemy.
# This is essential to create the database schema before performing any operations.
# It ensures that the database tables and relationships are set up according to the defined models.
models.Base.metadata.create_all(bind=engine)
