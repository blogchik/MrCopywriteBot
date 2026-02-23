"""Generation, Variant, Review, Suggestion, and GenerationVersion models."""

from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import JSON, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Generation(Base):
    __tablename__ = "generations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    use_case: Mapped[str] = mapped_column(String(50))
    language: Mapped[str] = mapped_column(String(5))
    settings_snapshot: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    input_snapshot: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    user: Mapped[User] = relationship(back_populates="generations")  # noqa: F821
    variants: Mapped[list[Variant]] = relationship(back_populates="generation")
    review: Mapped[Review | None] = relationship(back_populates="generation", uselist=False)
    versions: Mapped[list[GenerationVersion]] = relationship(back_populates="generation")


class Variant(Base):
    __tablename__ = "variants"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    generation_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("generations.id"))
    key: Mapped[str] = mapped_column(String(1))  # "A" or "B"
    text: Mapped[str] = mapped_column(Text)
    meta: Mapped[dict | None] = mapped_column(JSON, nullable=True)

    generation: Mapped[Generation] = relationship(back_populates="variants")


class Review(Base):
    __tablename__ = "reviews"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    generation_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("generations.id"), unique=True)
    score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    issues: Mapped[list | None] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    generation: Mapped[Generation] = relationship(back_populates="review")
    suggestions: Mapped[list[Suggestion]] = relationship(back_populates="review")


class Suggestion(Base):
    __tablename__ = "suggestions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    review_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("reviews.id"))
    type: Mapped[str] = mapped_column(String(50))
    label: Mapped[str] = mapped_column(String(255))
    payload: Mapped[dict | None] = mapped_column(JSON, nullable=True)

    review: Mapped[Review] = relationship(back_populates="suggestions")


class GenerationVersion(Base):
    __tablename__ = "generation_versions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    generation_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("generations.id"))
    applied_suggestion_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("suggestions.id"), nullable=True)
    result_text: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    generation: Mapped[Generation] = relationship(back_populates="versions")
    applied_suggestion: Mapped[Suggestion | None] = relationship()
