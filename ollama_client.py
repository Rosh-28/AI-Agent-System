import requests
import os
import dotenv
dotenv.load_dotenv()

OLLAMA_URL = os.getenv("Ollama_URL")
MODEL = os.getenv("Ollama_Model")

def call_ollama(prompt: str) -> str:
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        },
        timeout=60
    )
    return response.json()["response"]
