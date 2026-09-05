from fastapi import APIRouter
from app.api.routes import health, members, trainers, workflow

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(members.router)
api_router.include_router(trainers.router)
api_router.include_router(workflow.router)
