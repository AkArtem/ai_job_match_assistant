import json
import os
from src.extraction.extractor import extract_job
import time

with open("data/raw/jobs.json", "r", encoding="utf-8") as f:
    jobs = json.load(f)

result_path = "data/processed/jobs_extracted.json"
if os.path.exists(result_path):
    with open(result_path, "r", encoding="utf-8") as f:
        result = json.load(f)
else:
    result = []

existing_ids = {item["id"] for item in result}
failed = []

for job in jobs:
    if job["id"] in existing_ids:
        print("skip", job["id"])
        continue

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
        failed.append(job["id"])
        continue
    extracted.id = job["id"]
    extracted.source = job["source"]
    extracted.url = job["url"]
    
    result.append(extracted.model_dump())
    existing_ids.add(job["id"])
    print(job["id"], extracted.title, "|", extracted.company)
    
with open(result_path, "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

with open("data/processed/extraction_report.json", "w", encoding="utf-8") as f:
    json.dump({"total": len(jobs), "ok": len(result), "failed": failed}, f, ensure_ascii=False, indent=2)