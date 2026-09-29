## AI Job Match Assistant

AI Job Match Assistant is a small, evaluated RAG project for comparing real job postings with a candidate profile. It extracts structured requirements from unstructured vacancy text, uses embeddings to retrieve relevant roles, applies hard-fit checks such as language and working hours, and generates a clear match explanation with skill gaps.

The project is built step by step with Python, Pydantic, Gemini, sentence-transformers, ChromaDB, and Streamlit. The goal is not just to make a chatbot, but to understand where retrieval and generation succeed or fail. Evaluation will use real application outcomes wherever possible.

The Gemini API key should be stored in a local `.env` file and never committed to Git.
