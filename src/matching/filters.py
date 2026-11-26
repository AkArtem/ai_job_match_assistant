def german_to_rank(text):
    if not text or len(text) == 0:
        return None
    text = text.lower()

    if ("oder englisch" in text or "oder deutsch" in text
            or "or english" in text or "or german" in text):
        return None
    if "fließend" in text or "verhandlungssicher" in text:
        return 6
    elif "sehr gut" in text or "very good" in text:
        return 5
    elif "gut" in text:
        return 4
    elif "c2" in text:
        return 6
    elif "c1" in text:
        return 5
    elif "b2" in text:
        return 4
    elif "b1" in text:
        return 3
    elif "a2" in text:
        return 2
    elif "a1" in text:
        return 1
    return None

def hard_filter(jobs, profile): 
    LEVEL_TO_RANK = {"A1": 1, "A2": 2, "B1": 3, "B2": 4, "C1": 5, "C2": 6}
    rank_profile = LEVEL_TO_RANK.get(profile.german_level, 0)
    kept = []
    removed = []
    for job in jobs:
        job_german_rank = german_to_rank(job.get("min_german", ""))
        if job_german_rank is not None and job_german_rank > rank_profile:
            removed.append((job.get("id"), "german_level"))
            continue
        employment_type = (job.get("employment_type") or "").lower().replace("_", "-")
        if employment_type in {"full-time", "vollzeit"}:
            removed.append((job.get("id"), "employment_type"))
            continue
        if job.get("min_hours_per_week") is not None and job.get("min_hours_per_week") > profile.max_hours_per_week:
            removed.append((job.get("id"), "max_hours_per_week"))
            continue
        kept.append(job)
    return kept, removed

if __name__ == "__main__":
    from src.matching.profile import MY_PROFILE
    from src.loader import load_jobs

    jobs, _ = load_jobs()
    kept, removed = hard_filter(jobs, MY_PROFILE)
    print('--- Kept jobs ---')
    print(f"Kept {len(kept)} jobs: {[j['id'] for j in kept]}")
    print('--- Removed jobs ---')
    print(f"Removed {len(removed)} jobs: {removed}")