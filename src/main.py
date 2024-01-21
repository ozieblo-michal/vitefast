from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from route import auth, files, routes, route_limiter

import logging
from datetime import datetime, timedelta

# from mangum import Mangum

import os


from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded


from configure_logger import configure_logger

logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)

current_datetime = datetime.now()

date_str = current_datetime.strftime("%Y-%m-%d")
hour_str = current_datetime.strftime("%H:00")

next_hour = current_datetime + timedelta(hours=1)
next_hour_str = next_hour.strftime("%H:00")

timestamp = f"{date_str} {hour_str}-{next_hour_str}"

log_path = f"logs/{timestamp}.log"

bucket_name = os.getenv("S3_BUCKET_NAME")

logger = configure_logger(log_path, bucket_name)

# from auth.auth import pwd_context
# print(f'{pwd_context.hash("muminek")}')


app = FastAPI()

app.state.limiter = route_limiter.limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


# handler = Mangum(app)

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
    # uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

    uvicorn.run("main:app", host="0.0.0.0", port=80)
    # Można również uruchomić serwer z wieloma workerami, ale bez opcji przeładowania.
    # uvicorn.run("main:app", host="127.0.0.1", port=8000, workers=2)
