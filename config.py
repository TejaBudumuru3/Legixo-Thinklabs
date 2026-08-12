import os
from dotenv import load_dotenv
from google import genai
from pinecone import Pinecone

load_dotenv()

PINECONE_INDEX_NAME = 'legixo-corpus'

PINECONE_API_KEY = os.getenv('PINECONE_API')
GEMINI_API_KEY = os.getenv('GEMINI_API')
pc = Pinecone(PINECONE_API_KEY)
ai_client = genai.Client(api_key=GEMINI_API_KEY)