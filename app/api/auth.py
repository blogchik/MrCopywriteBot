"""Auth endpoints."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.user import User
from app.schemas.auth import TelegramAuth, UserRead

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/telegram", response_model=UserRead, status_code=status.HTTP_200_OK)
async def auth_telegram(
    payload: TelegramAuth,
    db: AsyncSession = Depends(get_db),
) -> User:
    """Authenticate via Telegram; creates the user on first login."""
    result = await db.execute(select(User).where(User.telegram_id == payload.telegram_id))
    user = result.scalar_one_or_none()

    if user is None:
        user = User(telegram_id=payload.telegram_id, locale="uz")
        db.add(user)
        await db.commit()
        await db.refresh(user)

    return user
