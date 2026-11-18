# AI Job Match Assistant

A RAG project that compares real job postings with a candidate profile. It extracts structured requirements from unstructured vacancy text, retrieves relevant roles with multilingual embeddings, applies hard-fit checks (language, working hours, employment type), and will generate a match explanation with skill gaps.

The goal is not just a chatbot, but to understand where retrieval and generation succeed or fail. Evaluation will use my own real "would apply / fits" labels.

**Status: work in progress** Numbers below are measured on 20 vacancies only and are indicative, not conclusions.

## Pipeline

1. **Extraction**: vacancy text -> Gemini (`gemini-3.1-flash-lite`, temperature 0) -> validated Pydantic `Job` (`src/extraction`).
2. **Embeddings**: `paraphrase-multilingual-MiniLM-L12-v2`, 384-dim vectors (`src/retrieval/embedder.py`). Each job is turned into a short text (title, skills, education, experience, location), because the model truncates long input.
3. **Vector store**: ChromaDB, cosine distance, `upsert` by job id so re-indexing does not create duplicates (`src/retrieval/store.py`).
4. **Search**: query -> same model -> top-n by cosine similarity (`search` in `store.py`).
5. **Hard filters** (planned): German level, full-time, minimum hours. Kept separate from semantic search on purpose.
6. **Match explanation** (planned): LLM with structured output.
7. **Evaluation** (planned): labelled vacancies, tune/holdout split, baselines (skill overlap, BM25).

## Findings so far

- **Model choice.** EN<->DE similarity of the same sentence: multilingual model 0.93 / 0.92 / 0.82, English-only `all-MiniLM-L6-v2` 0.57 / 0.39 / 0.16. Vacancies come in German and English, so the multilingual model is used.
- **Semantic search ignores seniority, language and employment type.** For the query "Werkstudent data analytics Python SQL" the top result was a Senior Data Analyst role. This is why hard filters are a separate step.
- **Similarity is not an absolute score.** An unrelated query ("warehouse worker forklift") still gave ~0.24 for its best match, so no fixed threshold is used; results are ranked.

## Setup

```
pip install -r requirements.txt
```

Create a `.env` file with `GEMINI_API_KEY=...` (never commit it).

```
python run_extraction.py          # extract structured jobs
python -m src.retrieval.store     # build the vector index
python playground_search.py       # try a search
```

## Limitations (so far)

- 20 vacancies, one candidate profile (mine), so results are not general.
- Extraction quality is not yet measured; some fields (language level, hours) are often missing in the source text.
