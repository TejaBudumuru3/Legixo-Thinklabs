import os
from config import pc, PINECONE_INDEX_NAME

try:
    index = pc.Index(PINECONE_INDEX_NAME)
except Exception as e:
    print(f" Warning: Pinecone index '{PINECONE_INDEX_NAME}' not found. You must run ingest.py first!")
    index = None

def upsert_vectors(vector_batch: list):
    if index is None:
        raise RuntimeError("Cannot upsert: Index does not exist.")
   
    index.upsert(vectors=vector_batch)

def query_index(vector: list[float], top_k: int = 3):
    if index is None:
        raise RuntimeError("Cannot upsert: Index does not exist.")
   
    result = index.query(vector=vector, top_k=top_k, include_metadata=True)
    return result.get("matches", [])