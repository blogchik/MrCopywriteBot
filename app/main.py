"""FastAPI application entry point."""

from __future__ import annotations

from fastapi import FastAPI

from app.api.router import api_router
from app.config import settings

app = FastAPI(
    title=settings.app_name,
    description="AI-powered copywriting platform – generates social-media copy in UZ/RU/EN with A/B variants, critic evaluation, and one-click improvements.",
    version="0.1.0",
)

app.include_router(api_router)
