import os
import google.generativeai as genai
from dotenv import load_dotenv
from src.extraction.models import Job

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.0-flash")
prompt = "Extract structured job posting data from the raw text. If a field is not explicitly mentioned in the text, return null(for lists, return an empty list). Do not guess or invent values."

def extract_job(raw_text: str) -> Job:
    response = model.generate_content(f"{prompt}\n\nJob posting text:\n{raw_text}", generation_config=genai.GenerationConfig(response_mime_type="application/json", response_schema=Job))
    job_data = response.parsed
    job_data.raw_text = raw_text
    return job_data