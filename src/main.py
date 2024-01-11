from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from route import auth, files, routes

import logging
from datetime import datetime, timedelta

#from mangum import Mangum


from configure_logger import configure_logger

logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)

current_datetime = datetime.now()

date_str = current_datetime.strftime('%Y-%m-%d')
hour_str = current_datetime.strftime('%H:00')

next_hour = current_datetime + timedelta(hours=1)
next_hour_str = next_hour.strftime('%H:00')

timestamp = f"{date_str} {hour_str}-{next_hour_str}"

log_path = f"logs/{timestamp}.log"

logger = configure_logger(log_path)

# from auth.auth import pwd_context
# print(f'{pwd_context.hash("muminek")}')


app = FastAPI()

#handler = Mangum(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(routes.router, prefix="/dummy")
app.include_router(auth.router)
app.include_router(files.router)


# Uruchomienie serwera Uvicorn, jeśli plik jest uruchamiany jako główny program.
if __name__ == "__main__":
    import uvicorn
    # Argument `reload=True` pozwala na automatyczne przeładowanie serwera przy zmianie kodu.
    # uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
    # Można również uruchomić serwer z wieloma workerami, ale bez opcji przeładowania.
    # uvicorn.run("main:app", host="127.0.0.1", port=8000, workers=2)
