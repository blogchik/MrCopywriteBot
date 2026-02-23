"""Billing schemas."""

from __future__ import annotations

import uuid
from datetime import datetime

from pydantic import BaseModel


class PlanRead(BaseModel):
    id: str
    name: str
    price: float
    daily_limit: int
    features: list[str] = []


class SubscribeRequest(BaseModel):
    plan_id: str
    payment_provider: str  # "stars" | "stripe" | "payme" | "crypto"


class EntitlementRead(BaseModel):
    id: uuid.UUID
    plan: str
    active_until: datetime | None = None
    daily_limit: int
    relaxed_safety: bool

    model_config = {"from_attributes": True}
