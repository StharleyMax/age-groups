"""Age Group Schemas."""

from pydantic import BaseModel


class AgeGroup(BaseModel):
    """Age Group Schema."""

    min_age: int
    max_age: int


class AgeGroupRequest(AgeGroup):
    """Age Group Request Schema."""


class AgeGroupResponse(AgeGroup):
    """Age Group Response Schema."""

    id: str
