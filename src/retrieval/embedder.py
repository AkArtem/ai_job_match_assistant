from sentence_transformers import SentenceTransformer
import json
model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
def job_to_text(job):
    result =[]
    if job.get("title"):
        result.append(job.get("title"))
    if job.get("required_skills"):
        result.append(", ".join(job.get("required_skills") or []))
    if job.get("education"):
        result.append(job.get("education"))
    if job.get("experience"):
        result.append(job.get("required_experience"))
    if job.get("location"):
        result.append(job.get("location"))
    all_job = ", ".join(result)
    return all_job

def embed(texts):
    return model.encode(texts)
        
if __name__ == "__main__":
    data = json.load(open("data/processed/jobs_extracted.json", "r", encoding="utf-8"))
    text = job_to_text(data[0])
    embeddings = embed([text])
    print(f"Embedding for job '{text}': {len(embeddings[0])}")