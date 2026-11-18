import json
import chromadb
from src.retrieval.embedder import job_to_text, embed

client = chromadb.PersistentClient(path="data/chroma")
collection = client.get_or_create_collection(name="jobs", metadata={"hnsw:space": "cosine"})

def make_metadata(job):
    metadata = {
        "title": job.get("title") or "",
        "company": job.get("company") or "",
        "location": job.get("location") or "",
        "work_model": job.get("work_model") or "",
        "employment_type": job.get("employment_type") or "",
        "min_german": job.get("min_german") or "",
        "min_english": job.get("min_english") or "",
        "min_hours_per_week": (job.get("min_hours_per_week") if job.get("min_hours_per_week") is not None else -1),
        "max_hours_per_week": (job.get("max_hours_per_week") if job.get("max_hours_per_week") is not None else -1),
        "url": job.get("url") or "",
    }
    return metadata

def add_jobs(jobs, collection=collection):
    texts = [job_to_text(job) for job in jobs]
    vectors = embed(texts)
    vectors = vectors.tolist()
    collection.upsert(
        ids=[job.get("id") or "" for job in jobs],  
        documents=texts,
        metadatas=[make_metadata(job) for job in jobs],
        embeddings=vectors
    )

if __name__ == "__main__":
    with open("data/processed/jobs_extracted.json", "r", encoding="utf-8") as f:
        jobs = json.load(f)
    add_jobs(jobs)
    print(collection.count())