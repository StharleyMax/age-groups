"""Age groups endpoints."""

from http import HTTPStatus

from fastapi import APIRouter

router = APIRouter(prefix="/age-groups", tags=["Age groups"])


@router.post("/", status_code=HTTPStatus.CREATED)
async def create(input: dict):
    """Add a new age group."""
    return input
