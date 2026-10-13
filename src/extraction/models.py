from pydantic import BaseModel, Field
from typing import Literal
class Job(BaseModel):
    id: str | None = None
    source: str | None = None
    url: str | None = None
    raw_text: str
    title: str | None = None
    company: str | None = None
    location: str | None = None
    work_model: Literal["onsite", "hybrid", "remote"] | None = None
    required_experience: str | None = None
    employment_type: str | None = None
    required_skills: list[str] = Field(default_factory=list)
    preferred_skills: list[str] = Field(default_factory=list)
    min_hours_per_week: int | None = None
    max_hours_per_week: int | None = None
    min_german: str | None = None
    min_english: str | None = None
    education: str | None = None
    expected_salary: str | None = None
