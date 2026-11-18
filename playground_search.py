from src.retrieval.store import search

query = "Werkstudent data analytics Python SQL"
for r in search(query, n=5):
    print(r["id"], round(r["similarity"], 3), r["title"], "|", r["company"])

print("---- 20 results, ranks of 007/008/009/011")
all_results = search(query, n=20)
for rank, r in enumerate(all_results, start=1):
    if r["id"] in ("007", "008", "009", "011"):
        print(rank, r["id"], round(r["similarity"], 3), r["title"])

print("---- sanity query")
for r in search("warehouse worker forklift", n=3):
    print(r["id"], round(r["similarity"], 3), r["title"])