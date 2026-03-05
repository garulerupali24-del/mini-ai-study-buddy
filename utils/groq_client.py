import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

def get_client():
    api_key = os.getenv("GROQ_API_KEY")
    return Groq(api_key=api_key)
