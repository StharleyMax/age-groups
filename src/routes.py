"""Routes module for the FastAPI application."""

from fastapi import APIRouter, FastAPI

from src.domains.age_groups.api.endpoints import router as age_groups_router
from src.domains.enrollments.api.endpoints import router as enrollments_router


def register(app: FastAPI):
    """
    Register all routers for the FastAPI application.

    :param app: FastAPI application instance.
    """
    main_router = APIRouter(prefix="/api")
    main_router.include_router(age_groups_router)
    main_router.include_router(enrollments_router)

    app.include_router(main_router)
