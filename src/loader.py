import json
from pydantic import ValidationError
from src.extraction.models import Job

def load_jobs(path="data/processed/jobs_extracted.json"):
    count = 0
    results = []
    ids = []
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    for item in data:
        try:
            job = Job.model_validate(item)
            results.append(job.model_dump())
        except ValidationError:
            count += 1
            ids.append(item.get("id", "unknown"))
    print(f"Loaded {len(results)} jobs with {count} errors.")
    print(f"Invalid job IDs: {ids}")
    return results, ids
if __name__ == "__main__":
    loaded_jobs, ids = load_jobs()
    print(f"Valid: {len(loaded_jobs)}, Invalid: {len(ids)}")