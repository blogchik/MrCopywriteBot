"""Generation endpoints (generate, review, improve, history)."""

from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database import get_db
from app.models.generation import Generation, Review, Suggestion, Variant
from app.schemas.generation import GenerationCreate, GenerationRead

router = APIRouter(tags=["generation"])


@router.post("/generate", response_model=GenerationRead, status_code=status.HTTP_201_CREATED)
async def create_generation(
    payload: GenerationCreate,
    user_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> Generation:
    """Create a new copy generation (placeholder – LLM call to be wired later)."""
    generation = Generation(
        user_id=user_id,
        use_case=payload.use_case,
        language=payload.language,
        settings_snapshot=payload.settings,
        input_snapshot={"text": payload.input_text},
    )
    db.add(generation)
    await db.flush()

    # Placeholder variants – will be replaced by LLM output
    for key in ("A", "B"):
        db.add(Variant(generation_id=generation.id, key=key, text=f"[placeholder {key}]"))

    await db.commit()

    result = await db.execute(
        select(Generation)
        .options(selectinload(Generation.variants), selectinload(Generation.review))
        .where(Generation.id == generation.id)
    )
    return result.scalar_one()


@router.get("/generation/{generation_id}", response_model=GenerationRead)
async def get_generation(
    generation_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> Generation:
    result = await db.execute(
        select(Generation)
        .options(
            selectinload(Generation.variants),
            selectinload(Generation.review).selectinload(Review.suggestions),
        )
        .where(Generation.id == generation_id)
    )
    gen = result.scalar_one_or_none()
    if gen is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Generation not found")
    return gen


@router.get("/history", response_model=list[GenerationRead])
async def list_history(
    user_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> list[Generation]:
    result = await db.execute(
        select(Generation)
        .options(selectinload(Generation.variants))
        .where(Generation.user_id == user_id)
        .order_by(Generation.created_at.desc())
        .limit(50)
    )
    return list(result.scalars().all())
