"""Endpoints for managing enrollments with age validation."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field, field_validator
from pydantic.types import StringConstraints

from src.domains.enrollments.services.enrollment_service import EnrollmentService
from src.shared.dependencies import get_enrollment_service

router = APIRouter(prefix="/enrollments", tags=["Enrollments"])


class EnrollmentCreate(BaseModel):
    """Schema for enrollment creation."""

    name: str = Field(..., min_length=3, max_length=100)
    age: int = Field(..., gt=0, lt=120)
    cpf: Annotated[str, StringConstraints(pattern=r"^\d{11}$")]

    @field_validator("cpf")
    def validate_cpf(cls, v: str) -> str:
        """Additional CPF validation."""
        if len(v) != 11 or not v.isdigit():
            raise ValueError("CPF must contain exactly 11 digits")

        # Adicione aqui validação de CPF real se necessário
        # Exemplo simplificado de validação de dígitos verificadores
        if v == v[0] * 11:  # Verifica se todos os dígitos são iguais
            raise ValueError("Invalid CPF")

        return v


class EnrollmentResponse(BaseModel):
    """Schema for enrollment response."""

    cpf: str
    name: str
    age: int
    status: str
    created_at: str
    updated_at: str
    age_group_id: str

    class Config:
        from_attributes = True


@router.post("/", response_model=EnrollmentResponse, status_code=status.HTTP_201_CREATED)
async def create_enrollment(
    enrollment: EnrollmentCreate,
    service: EnrollmentService = Depends(get_enrollment_service),
):
    """Create a new enrollment with age validation."""
    try:
        return service.create(enrollment.dict())
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))


@router.get("/{cpf}", response_model=EnrollmentResponse)
async def get_enrollment(
    cpf: str,
    service: EnrollmentService = Depends(get_enrollment_service),
):
    """Get enrollment by CPF."""
    enrollment = service.get({"cpf": cpf})
    if not enrollment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Enrollment not found")
    return enrollment
