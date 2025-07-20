import os
import dotenv
import numpy as np
import google.generativeai as genai


import os
from dotenv import load_dotenv  # ✅ Load from .env file

# ✅ Load environment variables from .env
load_dotenv()

try:
    import faiss  # This requires Python <= 3.10 and proper setup
except ModuleNotFoundError:
    raise ImportError("❌ FAISS is not installed. Use `chromadb` instead or set Python 3.10 in runtime.txt.")

# ✅ Get API key from environment (works with .env, GitHub Secrets, and Streamlit Cloud)
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError("❌ GOOGLE_API_KEY not found in environment.")

# Configure Gemini embedding model
genai.configure(api_key=GOOGLE_API_KEY)
embedding_model = "models/embedding-001"

# In-memory FAISS index and storage
index = None
stored_text_chunks = []

def store_in_vector_db(text_chunks):
    global index, stored_text_chunks

    if not text_chunks:
        raise ValueError("No text chunks provided.")

    embeddings = []
    for chunk in text_chunks:
        try:
            response = genai.embed_content(
                model=embedding_model,
                content=chunk,
                task_type="retrieval_document"
            )
            embeddings.append(response["embedding"])
        except Exception as e:
            print(f"❌ Failed to embed chunk: {chunk[:50]}...\nError: {e}")

    if not embeddings:
        raise ValueError("No valid embeddings generated.")

    embedding_matrix = np.array(embeddings).astype("float32")
    embedding_dim = embedding_matrix.shape[1]

    if index is None:
        index = faiss.IndexFlatL2(embedding_dim)

    index.add(embedding_matrix)
    stored_text_chunks.extend(text_chunks)

    print(f"✅ Stored {len(embeddings)} vectors in FAISS.")

def query_vector_db(query, k=3):
    global index, stored_text_chunks

    if index is None or index.ntotal == 0:
        raise ValueError("⚠️ Vector database is empty. Please store documents first.")

    try:
        query_embedding = genai.embed_content(
            model=embedding_model,
            content=query,
            task_type="retrieval_query"
        )["embedding"]
    except Exception as e:
        raise RuntimeError(f"❌ Failed to embed query: {e}")

    query_vector = np.array([query_embedding]).astype("float32")
    distances, indices = index.search(query_vector, k)
    results = [stored_text_chunks[i] for i in indices[0] if i < len(stored_text_chunks)]
    return results
