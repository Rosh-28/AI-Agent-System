import json
import requests
import os
import dotenv
dotenv.load_dotenv()

OLLAMA_URL = os.getenv("OLLAMA_URL")
MODEL = os.getenv("OLLAMA_MODEL")

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

    result = response.text.strip()
    for line in reversed(result.splitlines()):
        try:
            data = json.loads(line)
            if "response" in data:
                return data["response"]
        except json.JSONDecodeError:
            continue
    return result
