import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_set_config() -> None:
    async with AsyncClient(base_url="http://127.0.0.1:8000") as client:
        response = await client.post("/config/test_key", json="test_value")

    assert response.status_code == 200

    assert response.json() == {
        "message": "Test_key configuration registered successfully"
    }


@pytest.mark.asyncio
async def test_get_config() -> None:

    async with AsyncClient(base_url="http://127.0.0.1:8000") as client:
        response = await client.get("/config/test_key")

    assert response.status_code == 200

    assert response.json() == {"key": "test_key", "value": "test_value"}


@pytest.mark.asyncio
async def test_get_nonexistent_config() -> None:

    async with AsyncClient(base_url="http://127.0.0.1:8000") as client:
        response = await client.get("/config/nonexistent_key")

    assert response.status_code == 200

    assert response.json() == {"error": "Key not found"}
