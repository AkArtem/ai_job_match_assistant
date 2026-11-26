from src.loader import load_jobs
from src.retrieval.store import search, collection
from src.matching.filters import hard_filter
from src.matching.profile import MY_PROFILE

def profile_to_text(profile):
    text = ", ".join(profile.skills)
    summary = profile.summary + " Skills: " + text
    return summary


def find_matches(profile, n=3, use_filter=True):
    jobs, _ = load_jobs()
    jobs_by_id = {job["id"]: job for job in jobs}
    
    results = search(profile_to_text(profile), n=collection.count())
    ordered = [jobs_by_id[r["id"]] for r in results]
    if use_filter:
        ordered, removed = hard_filter(ordered, profile)
    similarity = {r["id"]: r["similarity"] for r in results}
    return [{"id": job["id"], "title": job["title"], "company": job["company"], "similarity": similarity[job["id"]]} for job in ordered[:n]]
if __name__ == "__main__":
    print(profile_to_text(MY_PROFILE))
    print(find_matches(MY_PROFILE, n=5, use_filter=True))
    print(find_matches(MY_PROFILE, n=5, use_filter=False))