import json
from src.extraction.extractor import extract_job
import time

with open("data/raw/jobs.json", "r", encoding="utf-8") as f:
    jobs = json.load(f)
result = []
for job in jobs:
    print("Processing job:", job["id"])
    extracted = None
    for attempt in range(3):
        try:
            extracted = extract_job(job["raw_text"])
            break
        except Exception as e:
            print("error", job["id"], "attempt", attempt + 1, e)
            time.sleep(10)
    if not extracted:
        print("Failed to extract job data for:", job["id"])
        continue
    extracted.id = job["id"]
    extracted.source = job["source"]
    extracted.url = job["url"]
    
    result.append(extracted.model_dump())
    print(job["id"], extracted.title, "|", extracted.company)
    
with open("data/processed/jobs_extracted.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)