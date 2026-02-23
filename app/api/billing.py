"""Billing endpoints."""

from __future__ import annotations

from fastapi import APIRouter

from app.schemas.billing import PlanRead

router = APIRouter(prefix="/billing", tags=["billing"])

# Static plans – will move to DB/admin later
PLANS: list[PlanRead] = [
    PlanRead(id="free", name="Free", price=0, daily_limit=2, features=["2 generations/day"]),
    PlanRead(id="pro", name="Pro", price=9.99, daily_limit=50, features=["50 generations/day", "Relaxed safety"]),
]


@router.get("/plans", response_model=list[PlanRead])
async def list_plans() -> list[PlanRead]:
    return PLANS
