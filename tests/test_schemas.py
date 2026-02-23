"""Schema validation tests."""

from __future__ import annotations

import uuid

from app.schemas.generation import GenerationCreate, VariantRead
from app.schemas.profiles import BrandProfileCreate


def test_generation_create_schema():
    data = GenerationCreate(
        language="uz",
        use_case="post",
        input_text="Test mahsulot haqida yozing",
    )
    assert data.language == "uz"
    assert data.settings is None


def test_variant_read_schema():
    data = VariantRead(id=uuid.uuid4(), key="A", text="Hello world")
    assert data.key == "A"
    assert data.meta is None


def test_brand_profile_create_schema():
    data = BrandProfileCreate(name="My brand", tone="friendly")
    assert data.name == "My brand"
    assert data.forbidden is None
