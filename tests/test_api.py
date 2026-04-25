"""Tests for the Mergington High School API"""
import pytest
from httpx import AsyncClient, ASGITransport
from src.app import app


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.mark.asyncio
async def test_get_activities():
    """Test fetching all activities"""
    # Arrange
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        # Act
        response = await client.get("/activities")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "Chess Club" in data
        assert "Programming Class" in data


@pytest.mark.asyncio
async def test_signup_student():
    """Test signing up a student for an activity"""
    # Arrange
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        # Act
        response = await client.post(
            "/activities/Chess Club/signup?email=newstudent@mergington.edu"
        )
        
        # Assert
        assert response.status_code == 200
        assert "Signed up" in response.json()["message"]


@pytest.mark.asyncio
async def test_duplicate_signup():
    """Test that duplicate signups are rejected"""
    # Arrange
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        # Act
        response = await client.post(
            "/activities/Chess Club/signup?email=michael@mergington.edu"
        )
        
        # Assert
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"]


@pytest.mark.asyncio
async def test_remove_participant():
    """Test removing a participant from an activity"""
    # Arrange
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        # Act
        response = await client.delete(
            "/activities/Chess Club/participants/daniel@mergington.edu"
        )
        
        # Assert
        assert response.status_code == 200
        assert "Removed" in response.json()["message"]


@pytest.mark.asyncio
async def test_activity_not_found():
    """Test signup for non-existent activity"""
    # Arrange
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        # Act
        response = await client.post(
            "/activities/Non Existent/signup?email=test@mergington.edu"
        )
        
        # Assert
        assert response.status_code == 404


@pytest.mark.asyncio
async def test_remove_unregistered_participant():
    """Test removing a participant that doesn't exist"""
    # Arrange
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        # Act
        response = await client.delete(
            "/activities/Chess Club/participants/nonexistent@mergington.edu"
        )
        
        # Assert
        assert response.status_code == 404