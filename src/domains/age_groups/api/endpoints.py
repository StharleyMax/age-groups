"""Age groups endpoints."""

from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from src.domains.age_groups.schema import AgeGroupRequest, AgeGroupResponse
from src.shared.auth import basic_auth
from src.shared.infra.database.repository.age_group_repository import AgeGroupRepository

router = APIRouter(prefix="/age-groups", tags=["Age groups"], dependencies=[Depends(basic_auth)])


@router.post("/", status_code=HTTPStatus.CREATED, response_model=AgeGroupResponse)
async def create(input: AgeGroupRequest) -> AgeGroupResponse:
    """Add a new age group."""
    repository = AgeGroupRepository()
    response = repository.create(item=input.model_dump())
    return AgeGroupResponse(**response)


@router.get("/{id}", response_model=AgeGroupResponse)
async def get(id: str) -> AgeGroupResponse:
    """Get an age group by ID."""
    repository = AgeGroupRepository()
    response = repository.get(key={"id": id})
    if not response:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND.value, detail="Age group not found")
    return AgeGroupResponse(**response)


@router.get("/", response_model=list[AgeGroupResponse])
async def list_all() -> list[AgeGroupResponse]:
    """List all age groups."""
    repository = AgeGroupRepository()
    response = repository.list()
    return [AgeGroupResponse(**item) for item in response]


@router.delete("/{id}", status_code=HTTPStatus.NO_CONTENT)
async def delete(id: str) -> None:
    """Delete an age group by ID."""
    repository = AgeGroupRepository()
    repository.delete(key={"id": id})
