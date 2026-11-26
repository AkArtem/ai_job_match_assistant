import json

with open("data/raw/jobs.json", "r", encoding="utf-8") as f:
    jobs = json.load(f)
with open("data/raw/new_jobs_nov.json", "r", encoding="utf-8") as f:
    new_jobs_nov = json.load(f)

existing_ids = {job["id"] for job in jobs}
added = 0
for job in new_jobs_nov:
    if job["id"] not in existing_ids:
        jobs.append(job)
        existing_ids.add(job["id"])
        added += 1
print(f"added {added}, skipped {len(new_jobs_nov) - added}")

with open("data/raw/jobs.json", "w", encoding="utf-8") as f:
    json.dump(jobs, f, ensure_ascii=False, indent=2)