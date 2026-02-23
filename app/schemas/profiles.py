"""Profile schemas."""

from __future__ import annotations

import uuid
from datetime import datetime

from pydantic import BaseModel


class BrandProfileCreate(BaseModel):
    name: str
    tone: str | None = None
    vocab: str | None = None
    forbidden: str | None = None
    examples: str | None = None


class BrandProfileRead(BrandProfileCreate):
    id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime

    model_config = {"from_attributes": True}


class AudienceProfileCreate(BaseModel):
    name: str
    persona: str | None = None
    pains: str | None = None
    desires: str | None = None
    style_prefs: str | None = None


class AudienceProfileRead(AudienceProfileCreate):
    id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime

    model_config = {"from_attributes": True}
