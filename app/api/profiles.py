"""Profile endpoints (Brand & Audience)."""

from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.profile import AudienceProfile, BrandProfile
from app.schemas.profiles import (
    AudienceProfileCreate,
    AudienceProfileRead,
    BrandProfileCreate,
    BrandProfileRead,
)

router = APIRouter(prefix="/profiles", tags=["profiles"])

# ---------------------------------------------------------------------------
# Brand profiles
# ---------------------------------------------------------------------------


@router.post("/brand", response_model=BrandProfileRead, status_code=status.HTTP_201_CREATED)
async def create_brand_profile(
    payload: BrandProfileCreate,
    user_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> BrandProfile:
    profile = BrandProfile(user_id=user_id, **payload.model_dump())
    db.add(profile)
    await db.commit()
    await db.refresh(profile)
    return profile


@router.get("/brand", response_model=list[BrandProfileRead])
async def list_brand_profiles(
    user_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> list[BrandProfile]:
    result = await db.execute(select(BrandProfile).where(BrandProfile.user_id == user_id))
    return list(result.scalars().all())


# ---------------------------------------------------------------------------
# Audience profiles
# ---------------------------------------------------------------------------


@router.post("/audience", response_model=AudienceProfileRead, status_code=status.HTTP_201_CREATED)
async def create_audience_profile(
    payload: AudienceProfileCreate,
    user_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> AudienceProfile:
    profile = AudienceProfile(user_id=user_id, **payload.model_dump())
    db.add(profile)
    await db.commit()
    await db.refresh(profile)
    return profile


@router.get("/audience", response_model=list[AudienceProfileRead])
async def list_audience_profiles(
    user_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> list[AudienceProfile]:
    result = await db.execute(select(AudienceProfile).where(AudienceProfile.user_id == user_id))
    return list(result.scalars().all())
