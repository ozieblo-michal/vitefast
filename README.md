# FastAPI - templates and exercises

```

src : Contains all the website code / source files
├── web : The FastAPI web layer / top layer
├── service : The business logic layer / intermediate layer
├── data : The storage interface layer / bottom layer
├── model : Pydantic model definitions / data aggregates definitions
├── fake : Stub data
├── test : Test scripts / various layers
├── db : Text and SQLite data sources for book examples
└── main.py : Sample top website file
```


## to run:

```zsh
poetry shell
poetry run python main.py
```

## tests:
```zsh
poetry run python -m pytest .
```

### Notes: 
- attention to what is the Pydantic model and what is SQLAlchemy for class instances
- Connecting SQLAlchemy and Pydantic models
- Using APIRouter in FastAPI
- Troubleshooting Python imports
