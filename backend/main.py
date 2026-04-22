from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from backend.api.router import api_router
from backend.config import get_settings
from backend.db import init_db

settings = get_settings()
app = FastAPI(title="SURAKSHA API", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "X-API-Key"],
)
app.include_router(api_router, prefix="/api")

frontend_dir = Path(__file__).resolve().parent.parent / "frontend"
if frontend_dir.exists():
    app.mount("/frontend", StaticFiles(directory=frontend_dir), name="frontend")


@app.on_event("startup")
def startup() -> None:
    init_db()


@app.middleware("http")
async def api_key_guard(request: Request, call_next):
    public_paths = {"/", "/health"}
    if request.url.path.startswith("/frontend") or request.url.path in public_paths:
        return await call_next(request)

    if request.url.path.startswith("/api"):
        supplied = request.headers.get("X-API-Key")
        if supplied != settings.api_key:
            return JSONResponse(status_code=401, content={"detail": "unauthorized"})

    return await call_next(request)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "env": settings.app_env}


@app.get("/")
def web_app() -> FileResponse:
    index = frontend_dir / "index.html"
    return FileResponse(index)
