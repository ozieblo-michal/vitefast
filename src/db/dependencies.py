from db.database import SessionLocal


def get_db():
    """Dependency function to obtain a database session.

    This function yields a SQLAlchemy session from a session factory upon
    request and closes it after use.

    Yields:
        Session: A SQLAlchemy session object to interact with the database.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
