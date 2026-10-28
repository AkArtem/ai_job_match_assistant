from sentence_transformers import SentenceTransformer, util

texts=["Data Analyst with SQL and Python", "SQL data analysis job", "Warehouse worker night shift", "Datenanalyst mit SQL und Python", "Stelle für SQL-Datenanalyse", "Lagerarbeiter Nachtschicht"]
models = [SentenceTransformer("all-MiniLM-L6-v2"),  SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")]
for model in models:
    vectors = model.encode(texts)
    for i in range(len(texts)//2):
        similarity = util.cos_sim(vectors[i], vectors[len(texts)//2 + i])
        print(f"Similarity between '{texts[i]}' and '{texts[len(texts)//2 + i]}': {float(similarity)}")