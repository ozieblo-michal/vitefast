import pytest
from fastapi import HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import model.models as models
import schema.schemas as schemas
# from service.services import get_dummy, get_dummies, create_dummy, delete_dummy, update_dummy
import service.services as services


@pytest.fixture(scope="function")
def db_session():
    engine = create_engine("sqlite:///:memory:", echo=True)
    models.Base.metadata.create_all(engine)  # Utworzenie tabel
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def test_modify_partially(db_session):
    test_dummy = models.Dummy(
        name="Test", description="Test Description", optional_field="Test Field"
    )
    db_session.add(test_dummy)
    db_session.commit()

    new_data = schemas.Dummy(
        name="Updated", description="Updated Description", optional_field=None
    )
    updated_dummy = services.modify_partially(
        dummy_id=test_dummy.id, dummy=new_data, db=db_session
    )

    assert updated_dummy.name == "Updated"
    assert updated_dummy.description == "Updated Description"
    assert updated_dummy.optional_field is None

    with pytest.raises(HTTPException) as exc_info:
        services.modify_partially(dummy_id=999, dummy=new_data, db=db_session)
    assert exc_info.value.status_code == 404
