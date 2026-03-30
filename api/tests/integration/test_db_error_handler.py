"""Integration tests for database error handling via HTTP endpoints."""

from unittest.mock import AsyncMock

import pytest
from fastapi import status
from httpx import ASGITransport, AsyncClient

from app.infrastructure.exceptions import DatabaseError, IntegrityConstraintError
from app.main import app


class TestDatabaseErrorHandler:
    """Test that database errors are translated to clean HTTP responses."""

    @pytest.fixture
    def client(self) -> AsyncClient:
        return AsyncClient(transport=ASGITransport(app=app), base_url="http://test")

    @pytest.mark.asyncio
    async def test_integrity_error_returns_409(self, client: AsyncClient) -> None:
        """Unique constraint violation should return 409 Conflict."""
        from app.routers import candidate_router

        # Create a mock service that raises the exception
        mock_service = AsyncMock()
        mock_service.create_candidate = AsyncMock(
            side_effect=IntegrityConstraintError(
                "duplicate key value violates unique constraint",
                constraint_type="unique",
            )
        )

        # Override the dependency - return the mock directly
        app.dependency_overrides[candidate_router.get_candidate_service] = (
            lambda: mock_service
        )

        try:
            response = await client.post(
                "/api/v1/candidates/",
                json={
                    "name": "Test User",
                    "email": "test@example.com",
                    "skills": ["Python"],
                },
            )
            assert response.status_code == status.HTTP_409_CONFLICT
            data = response.json()
            assert data["error_type"] == "unique"
        finally:
            app.dependency_overrides.clear()

    @pytest.mark.asyncio
    async def test_database_error_returns_500(self, client: AsyncClient) -> None:
        """Generic database error should return 500, not expose stack trace."""
        from app.routers import candidate_router

        # Create a mock service that raises the exception
        mock_service = AsyncMock()
        mock_service.create_candidate = AsyncMock(
            side_effect=DatabaseError("Connection failed")
        )

        app.dependency_overrides[candidate_router.get_candidate_service] = (
            lambda: mock_service
        )

        try:
            response = await client.post(
                "/api/v1/candidates/",
                json={
                    "name": "Test User",
                    "email": "test@example.com",
                    "skills": ["Python"],
                },
            )
            assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
            data = response.json()
            assert "detail" in data
            # Should NOT expose internal error details
            assert "Connection failed" not in data.get("detail", "")
        finally:
            app.dependency_overrides.clear()

    @pytest.mark.asyncio
    async def test_handler_does_not_expose_traceback(self, client: AsyncClient) -> None:
        """Verify that database errors don't leak internal details."""
        from app.routers import candidate_router

        # Create a mock service that raises the exception with sensitive data
        mock_service = AsyncMock()
        mock_service.create_candidate = AsyncMock(
            side_effect=DatabaseError(
                "Internal DB error with sensitive info",
                details={"table": "users", "query": "SELECT * FROM secret"},
            )
        )

        app.dependency_overrides[candidate_router.get_candidate_service] = (
            lambda: mock_service
        )

        try:
            response = await client.post(
                "/api/v1/candidates/",
                json={
                    "name": "Test User",
                    "email": "test@example.com",
                    "skills": ["Python"],
                },
            )
            response_text = response.text
            # Ensure no sensitive info leaks
            assert "Internal DB error" not in response_text
            assert "users" not in response_text
            assert "SELECT" not in response_text
        finally:
            app.dependency_overrides.clear()


class TestDatabaseErrorHandlerRegistration:
    """Verify the exception handler is properly registered."""

    def test_handler_registered(self) -> None:
        """Verify DatabaseError handler exists in exception handlers."""
        assert DatabaseError in app.exception_handlers