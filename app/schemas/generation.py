"""Generation schemas."""

from __future__ import annotations

import uuid
from datetime import datetime

from pydantic import BaseModel


class GenerationCreate(BaseModel):
    language: str
    use_case: str
    input_text: str
    settings: dict | None = None
    brand_profile_id: uuid.UUID | None = None
    audience_profile_id: uuid.UUID | None = None


class VariantRead(BaseModel):
    id: uuid.UUID
    key: str
    text: str
    meta: dict | None = None

    model_config = {"from_attributes": True}


class SuggestionRead(BaseModel):
    id: uuid.UUID
    type: str
    label: str
    payload: dict | None = None

    model_config = {"from_attributes": True}


class ReviewRead(BaseModel):
    id: uuid.UUID
    score: int | None = None
    issues: list | None = None
    suggestions: list[SuggestionRead] = []
    created_at: datetime

    model_config = {"from_attributes": True}


class GenerationRead(BaseModel):
    id: uuid.UUID
    use_case: str
    language: str
    settings_snapshot: dict | None = None
    input_snapshot: dict | None = None
    variants: list[VariantRead] = []
    review: ReviewRead | None = None
    created_at: datetime

    model_config = {"from_attributes": True}


class ImproveRequest(BaseModel):
    generation_id: uuid.UUID
    suggestion_id: uuid.UUID
    target_variant: str  # "A" or "B"


class GenerationVersionRead(BaseModel):
    id: uuid.UUID
    generation_id: uuid.UUID
    applied_suggestion_id: uuid.UUID | None = None
    result_text: str
    created_at: datetime

    model_config = {"from_attributes": True}
