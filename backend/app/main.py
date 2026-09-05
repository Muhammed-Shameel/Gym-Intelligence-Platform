from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import inspect

from app.api.router import api_router
from app.core.config import get_settings
from app.core.database import Base, engine, SessionLocal
from app.data.seed import seed_data
from app import models  # noqa: F401

settings = get_settings()

@asynccontextmanager
async def lifespan(_: FastAPI):
    print("DEBUG: Lifespan is running!")
    # Idempotent table creation and seeding
    try:
        db = SessionLocal()
        # Create tables only if they don't exist
        Base.metadata.create_all(bind=engine)
        seed_data(db)
        db.close()
    except Exception as e:
        print(f"Startup initialization warning/error (likely benign if DB exists): {e}")
    yield

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="GFIP deterministic Agentic AI Phase 1 starter foundation.",
    lifespan=lifespan,
)

print(f"DEBUG: CORS origins are: {settings.cors_origin_list}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)
