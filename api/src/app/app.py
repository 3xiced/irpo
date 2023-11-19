import time
from typing import Any, Callable

from .api.user import user_router
from .external.postgres import create_tables
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

app = FastAPI(
    title="RESTAPI",
    version="0.0.1",
    docs_url="/api/docs",
    swagger_ui_parameters={"defaultModelsExpandDepth": -1},
)


origins = ["http://localhost", "http://localhost:8080", "http://localhost:3000", "*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next: Callable) -> Any:
    start_time = time.time()
    response = await call_next(request)

    logger.info(
        f'method="{request.scope["method"]}" router="{request.scope["path"]}" '
        f"process_time={round(time.time() - start_time, 3)} "
        f"status_code={response.status_code}"
    )
    return response


@app.get(path="/api/ping", name="Ping api", status_code=200)
async def ping() -> str:
    return "ok"


@app.on_event("startup")
async def on_startup_event():
    await create_tables()


app.include_router(user_router)
