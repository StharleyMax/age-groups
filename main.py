"""Entry point for the FastAPI application."""

from src.app import create_app

app = create_app()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8010, reload=True, log_level="debug")
