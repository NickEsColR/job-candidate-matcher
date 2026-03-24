"""Application entrypoint — composition root."""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.settings import get_settings
from app.infrastructure.db import dispose_engine
from app.routers.candidate_router import router as candidate_router


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None, None]:
    """Startup / shutdown lifecycle manager."""
    settings = get_settings()
    print(f"🚀 Starting app on {settings.app_host}:{settings.app_port}")
    yield
    await dispose_engine()
    print("🛑 Shutting down")


def create_app() -> FastAPI:
    """Factory that builds and returns the FastAPI application."""
    settings = get_settings()

    app = FastAPI(
        title="Job Candidate Matcher",
        version="0.1.0",
        lifespan=lifespan,
        docs_url="/docs" if settings.debug else None,
        redoc_url="/redoc" if settings.debug else None,
    )

    # Mount routers
    app.include_router(candidate_router)

    @app.get("/health", tags=["health"])
    async def health_check() -> dict[str, str]:
        return {"status": "ok"}

    return app


app = create_app()

if __name__ == "__main__":
    import uvicorn

    settings = get_settings()
    uvicorn.run(
        "app.main:app",
        host=settings.app_host,
        port=settings.app_port,
        reload=settings.debug,
    )
