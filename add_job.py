import json

with open("data/raw/jobs.json", "r", encoding="utf-8") as f:
    jobs = json.load(f)
    
with open("data/raw/new_jobs.json", "r", encoding="utf-8") as f:
    new_jobs = json.load(f)
    
with open("data/raw/job_006.json", "r", encoding="utf-8") as f:
    job_006 = json.load(f)

jobs.extend(job_006)  
jobs.extend(new_jobs)
json.dump(jobs, open("data/raw/jobs.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)