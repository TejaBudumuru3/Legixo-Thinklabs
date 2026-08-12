import os
from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv
from config import pc, PINECONE_API_KEY, PINECONE_INDEX_NAME, ai_client
from google.genai import types
from app.pinecone_client import upsert_vectors
import hashlib

CHUNK_SIZE=250
OVERLAP=50

if PINECONE_INDEX_NAME not in pc.list_indexes().names():
    print(f"creating index '{PINECONE_INDEX_NAME}'")
    pc.create_index(
        name=PINECONE_INDEX_NAME,
        dimension=768,
        metric='cosine',
        spec=ServerlessSpec(cloud="aws", region='us-east-1')
    )

def chunk_text(text: str) -> list[str]:
    chunks = []
    step = CHUNK_SIZE - OVERLAP
    for i in range(0, len(text), step):
        chunk = text[i: i+CHUNK_SIZE]
        chunks.append(chunk)

    return chunks

def make_vector_id(source_path, chunk_index: int) -> str:
    raw = f"{source_path}:{chunk_index}"
    return hashlib.md5(raw.encode()).hexdigest()
  
if __name__ == "__main__":
    vector_batch = []
    files = os.listdir('corpus')
    for file in files:
        try:
            with open(os.path.join("corpus", file), 'r', encoding='utf-8') as f:
                content = f.read()
                chunks = chunk_text(content)
                
                print("calling gemini for embedding")
                result = ai_client.models.embed_content(
                    model="gemini-embedding-001",
                    contents=chunks,
                    config=types.EmbedContentConfig(output_dimensionality=768, task_type='RETRIEVAL_DOCUMENT'))

                print("organizing the chunks")
                if result.embeddings:
                    for i, chunk in enumerate(chunks):
                        chunk_id = make_vector_id(file, i)

                        vector = result.embeddings[i].values
                        vector_chunk = {
                            "id": chunk_id,
                            "values": vector,
                            "metadata": {
                                "text": chunk,
                                "source": file
                            }
                        }

                        vector_batch.append(vector_chunk)
                print(f"{file} is done moving to next file...")
        except Exception as e:
            print(f"Failed to process {file}. Error: {e}")
            continue
    try:
        if vector_batch:
            upsert_vectors(vector_batch)
            print("Ingestion completed")
    except Exception as e:
        print(f"Failed to upload to Pinecone! Error: {e}")

