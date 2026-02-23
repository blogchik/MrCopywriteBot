"""Billing endpoint tests."""

from __future__ import annotations

import pytest


@pytest.mark.anyio
async def test_list_plans(client):
    response = await client.get("/billing/plans")
    assert response.status_code == 200
    plans = response.json()
    assert len(plans) == 2
    ids = [p["id"] for p in plans]
    assert "free" in ids
    assert "pro" in ids
