from sqlalchemy import Column, Integer, String, Boolean

from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Dummy(Base):
    """
    Model representing the 'dummy' table in the database.

    This model is used to store information about 'Dummy' objects, with attributes such as id, name, description, and an optional field.

    Attributes:
        id (int): The unique identifier for each record, serving as the primary key of the table.
        name (str): The name of the Dummy object. It is a required field and cannot be NULL.
        description (str): A description of the Dummy object. It is a required field and cannot be NULL.
        optional_field (str): An additional, optional field that can be NULL.
    """

    __tablename__ = "dummy"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    optional_field = Column(String, nullable=True)


class User(Base):
    """
    Model representing the 'users' table in the database.

    This model is used for storing user information, including attributes like username, full name, email, password, and disabled status.

    Attributes:
        id (int): The unique identifier for each user, serving as the primary key of the table.
        username (str): The username of the user, which is unique and indexed.
        full_name (str): The full name of the user. It cannot be NULL.
        email (str): The email address of the user, which is unique and indexed.
        password (str): The encrypted password of the user. Ensure this is not exposed in API responses.
        disabled (bool): A flag indicating whether the user account is disabled. Defaults to False.
    """
    
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    disabled = Column(Boolean, default=False)
