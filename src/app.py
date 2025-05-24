"""App factory for FastAPI."""

from fastapi import FastAPI

from src import routes


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title="Age Groups API",
        version="1.0.0",
        description="An API for managing age groups.",
        docs_url="/docs",
    )

    routes.register(app)

    @app.get("/health", include_in_schema=False)
    async def health_check():
        return {"status": "ok"}

    return app
