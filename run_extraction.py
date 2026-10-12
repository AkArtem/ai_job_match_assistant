import json
from src.extraction.extractor import extract_job

with open("data/raw/jobs.json", "r", encoding="utf-8") as f:
    jobs = json.load(f)
result = []
for job in jobs:
    extracted = extract_job(job["raw_text"])
    extracted.id = job["id"]
    extracted.source = job["source"]
    extracted.url = job["url"]
    
    result.append(extracted.model_dump())
    print(job["id"], extracted.title, "|", extracted.company)
    
with open("data/processed/jobs_extracted.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)