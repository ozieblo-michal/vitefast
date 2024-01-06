# Module templates in FastAPI

#### Keywords: CRUD, REST API

## Purpose
This repository serves as a collection of templates for various tasks in FastAPI, aimed at facilitating rapid backend development for applications. It's also a training repository for understanding and implementing FastAPI features.

## About FastAPI
FastAPI is a modern, fast (high-performance) web framework for building APIs with Python 3.7+ based on standard Python type hints. The key features are:

- **Fast**: Very high performance, on par with NodeJS and Go (thanks to Starlette and Pydantic). One of the fastest Python frameworks available.
- **Fast to code**: Increase the speed to develop features by about 200% to 300%. 
- **Fewer bugs**: Reduce about 40% of human (developer) induced errors.
- **Intuitive**: Great editor support. Completion everywhere. Less time debugging.
- **Easy**: Designed to be easy to use and learn. Less time reading docs.
- **Short**: Minimize code duplication. Multiple features from each parameter declaration. Fewer bugs.
- **Robust**: Get production-ready code. With automatic interactive documentation.


## Package structure
```
src/
├── model/
    ├──models.py [Defines SQLAlchemy ORM models representing database tables.]
    └── __init__.py [Initializes the model package, allowing for its modules to be imported elsewhere.]
├── db/
    ├── database.py [Sets up and configures the database connection and session handling.]
    ├── fake_db.py [Provides a mock database for testing or development purposes.]
    └── __init__.py [Initializes the db package to enable database configurations.]
├── service/
    ├── dummy.py [Contains business logic or services related to 'Dummy' entities.]
    └── __init__.py [Initializes the service package for organizing business logic.]
├── schema/
    ├── schemas.py [Defines Pydantic models for data validation and serialization.]
    └── __init__.py [Initializes the schema package to encapsulate Pydantic models.]
├── route/
    ├── routes.py [Defines the API routes/endpoints for the application.]
    └── __init__.py [Initializes the route package, grouping the route modules.]
├── tests/
    ├── __init__.py [Initializes the tests package, aggregating test modules.]
    └── unit/
        ├── __init__.py [Initializes the unit testing subpackage within tests.]
        └── route/
            ├── __init__.py [Initializes the route testing module for unit tests.]
            └── test_route.py [Unit tests for route functionalities.]
└── main.py [The main entry point for the FastAPI application, defining API routes.]

```


## How to run the app

```zsh
poetry shell
poetry run python main.py
```

in web browser, open `http://localhost:8000/docs`

## How to run tests
```zsh
poetry run python -m pytest .
```
