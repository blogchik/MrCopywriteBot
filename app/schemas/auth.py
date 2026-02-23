"""Auth schemas."""

from __future__ import annotations

import uuid

from pydantic import BaseModel


class TelegramAuth(BaseModel):
    telegram_id: int
    first_name: str | None = None
    last_name: str | None = None
    username: str | None = None
    photo_url: str | None = None
    auth_date: int
    hash: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserRead(BaseModel):
    id: uuid.UUID
    telegram_id: int | None = None
    email: str | None = None
    locale: str

    model_config = {"from_attributes": True}
