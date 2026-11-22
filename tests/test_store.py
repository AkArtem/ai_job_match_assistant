import chromadb
from src.retrieval.store import add_jobs

def test_add_jobs_twice_no_duplicates():
    jobs = [
        {"id": "t1", "title": "Data Scientist", "required_skills": ["Python", "SQL"], "location": "Linz"},
        {"id": "t2", "title": "Excel Specialist", "required_skills": ["Excel"], "location": "Wien"},
    ]
    client = chromadb.EphemeralClient()
    collection = client.get_or_create_collection(name="test_jobs", metadata={"hnsw:space": "cosine"})

    add_jobs(jobs, collection=collection)
    count_after_first = collection.count()

    add_jobs(jobs, collection=collection)
    count_after_second = collection.count()

    assert count_after_first == len(jobs)
    assert count_after_second == count_after_first