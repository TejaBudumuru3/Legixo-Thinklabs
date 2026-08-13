import os
from dotenv import load_dotenv
from google import genai
from pinecone import Pinecone
from groq import Groq

load_dotenv()

PINECONE_INDEX_NAME = 'legixo-corpus'

PINECONE_API_KEY = os.getenv('PINECONE_API')
GEMINI_API_KEY = os.getenv('GEMINI_API')
GROQ_API_KEY = os.getenv('GROQ_API')

pc = Pinecone(PINECONE_API_KEY)
ai_client = genai.Client(api_key=GEMINI_API_KEY)
groq_client = Groq(api_key=GROQ_API_KEY)