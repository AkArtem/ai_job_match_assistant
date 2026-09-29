from pydantic import BaseModel
from typing import Optional

class Job(BaseModel):
    id: Optional[int] = None
    source: str | None = None
    url: str | None = None
    raw_text: str
    title: str | None = None
    company: str | None = None
    location: str | None = None
    remote: bool | None = None
    experience: str | None = None
    employment_type: str | None = None
    required_skills: list[str] = []
    preferred_skills: list[str] = []
    min_hours_per_week: int | None = None
    max_hours_per_week: int | None = None
    min_german: str | None = None
    min_english: str | None = None
    education: str | None = None
    expected_salary: float | None = None
