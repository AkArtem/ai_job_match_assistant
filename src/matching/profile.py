from typing import Literal
from pydantic import BaseModel, ValidationError

class CandidateProfile(BaseModel):
    german_level: Literal["A1", "A2", "B1", "B2", "C1", "C2"]
    english_level: Literal["A1", "A2", "B1", "B2", "C1", "C2"]
    max_hours_per_week: int
    skills: list[str]
    summary: str

MY_PROFILE = CandidateProfile(german_level="A2", english_level="C1", max_hours_per_week=20, skills=["Python", "Machine Learning", "Data Analysis", "SQL", "pandas", "scikit-learn", "streamlit"], summary="JKU AI student, projects in ML and data analysis, looking for a Werkstudent role in data/ML")
if __name__ == "__main__":
    print(MY_PROFILE)
    try:
        profile = CandidateProfile(german_level="D2", english_level="C1", max_hours_per_week=15, skills=["Python", "SQL", "Data Visualization"], summary="Experienced data analyst with a focus on Python and SQL.")
    except ValidationError as e:
        print("Error:", e)