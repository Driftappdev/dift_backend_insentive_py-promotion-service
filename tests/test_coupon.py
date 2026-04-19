import pytest
from httpx import AsyncClient
from app.main import app
from app.database import async_session, engine
from app.models.coupon import Base

import asyncio

@pytest.fixture(scope="module")
async def setup_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.mark.asyncio
async def test_create_coupon(setup_db):
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/coupons/", json={
            "code": "TEST10",
            "description": "Test Coupon",
            "discount_type": "percentage",
            "discount_value": 10.0,
            "valid_from": "2025-01-01T00:00:00",
            "valid_to": "2025-12-31T23:59:59"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == "TEST10"
        assert data["discount_value"] == 10.0
