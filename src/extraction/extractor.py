import os
import google.genai as genai
from dotenv import load_dotenv
from src.extraction.models import Job
from google.genai import types

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
prompt = """Extract structured job posting data from the raw text.

General rule:
- If a field is not explicitly mentioned in the text, return null (for lists, return an empty list). Do not guess or invent values.

required_skills and preferred_skills:
- required_skills: only skills and tools that the text states as required.
- Examples introduced by "e.g." or "such as" are NOT required skills.
- If the text lists alternatives ("Python, C#, JavaScript, or Java"), put them in preferred_skills, not in required_skills.
- Skills marked "preferably", "is a plus", "advantageous" or "bonus" go to preferred_skills.
- Do not list soft skills (communication, analytical thinking, teamwork) as skills.

required_experience:
- Take it only from the requirements text. Ignore level labels in the listing header such as "Berufserfahrung" or "Berufseinstieg".

work_model:
- Use "onsite", "hybrid" or "remote". "Homeoffice möglich", "mit Homeoffice" and "hybrid" all mean "hybrid". Return null if not mentioned.

Hours and languages:
- min_hours_per_week and max_hours_per_week: only numbers stated in the text.
- min_german and min_english: use a CEFR level (A1-C2) if given, otherwise copy the wording from the text.
"""


def extract_job(raw_text: str) -> Job:
    response = client.models.generate_content(model="gemini-3.1-flash-lite", contents=f"{prompt}\n\nJob posting text:\n{raw_text}", config=types.GenerateContentConfig(response_mime_type="application/json", response_schema=Job, temperature=0))
    job_data = response.parsed
    job_data.raw_text = raw_text
    return job_data
