from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from route import auth, files, route_limiter, crud

import uvicorn


import os


from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from configure_logger import configure_logger


logger = configure_logger()

logger.debug(f"Current working directory: {os.getcwd()}")

app = FastAPI()

app.state.limiter = route_limiter.limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(crud.router, prefix="/dummy")
app.include_router(auth.router, prefix="/auth")
app.include_router(files.router)


if __name__ == "__main__":
    if os.environ.get("RUNNING_IN_CONTAINER"):
        uvicorn.run("main:app", host="0.0.0.0", port=80, log_config=None)
    else:
        uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True, log_config=None)
