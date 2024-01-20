from sqlalchemy import Column, Integer, String

# from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Dummy(Base):
    """Model class representing a 'dummy' table in the database.

    This class extends `Base`, making it a model class that SQLAlchemy can map to a table.
    The table will store data about 'Dummy' objects with attributes id, name, and description.

    Attributes:
        id (int): The primary key, automatically generated, unique identifier for each record.
        name (str): The name attribute, a string that can be NULL.
        description (str): The description attribute, a string that can also be NULL.
    """

    __tablename__ = "dummy"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    optional_field = Column(String, nullable=True)
