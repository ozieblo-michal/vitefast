from fastapi import FastAPI

from route import auth, dummy

# from auth.auth import pwd_context
# print(f'dupa: {pwd_context.hash("muminek")}')


app = FastAPI()


app.include_router(dummy.router, prefix="/dummy")
app.include_router(auth.router)


# Uruchomienie serwera Uvicorn, jeśli plik jest uruchamiany jako główny program.
if __name__ == "__main__":
    import uvicorn

    # Argument `reload=True` pozwala na automatyczne przeładowanie serwera przy zmianie kodu.
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
    # Można również uruchomić serwer z wieloma workerami, ale bez opcji przeładowania.
    # uvicorn.run("main:app", host="127.0.0.1", port=8000, workers=2)
