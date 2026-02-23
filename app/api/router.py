"""Central API router that aggregates all sub-routers."""

from __future__ import annotations

from fastapi import APIRouter

from app.api.auth import router as auth_router
from app.api.billing import router as billing_router
from app.api.generation import router as generation_router
from app.api.health import router as health_router
from app.api.profiles import router as profiles_router

api_router = APIRouter()
api_router.include_router(health_router)
api_router.include_router(auth_router)
api_router.include_router(profiles_router)
api_router.include_router(generation_router)
api_router.include_router(billing_router)
