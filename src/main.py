from fastapi import FastAPI
from route import dummy

app = FastAPI()

app.include_router(dummy.router, prefix = "/dummy")



# Uruchomienie serwera Uvicorn, jeśli plik jest uruchamiany jako główny program.
if __name__ == "__main__":
    import uvicorn
    # Argument `reload=True` pozwala na automatyczne przeładowanie serwera przy zmianie kodu.
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
    # Można również uruchomić serwer z wieloma workerami, ale bez opcji przeładowania.
    # uvicorn.run("main:app", host="127.0.0.1", port=8000, workers=2)
