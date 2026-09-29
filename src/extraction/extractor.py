import os
import google.genai as genai
from dotenv import load_dotenv
from src.extraction.models import Job
from google.genai import types

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
prompt = "Extract structured job posting data from the raw text. If a field is not explicitly mentioned in the text, return null(for lists, return an empty list). Do not guess or invent values."

def extract_job(raw_text: str) -> Job:
    response = client.models.generate_content(model="gemini-3.1-flash-lite", contents=f"{prompt}\n\nJob posting text:\n{raw_text}", config=types.GenerateContentConfig(response_mime_type="application/json", response_schema=Job))
    job_data = response.parsed
    job_data.raw_text = raw_text
    return job_data