import os

import requests
from dotenv import load_dotenv

load_dotenv()


def _get_env(*names: str) -> str:
    for name in names:
        value = os.getenv(name)
        if value and value.strip():
            return value.strip()
    return ""


def generate_response(prompt: str) -> str:
    api_key = _get_env("GROQ_API_KEY", "GROQ_TOKEN")
    if not api_key:
        raise RuntimeError("Missing GROQ_API_KEY in environment variables.")

    model_name = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    data = {
        "model": model_name,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
    }

    response = requests.post(url, headers=headers, json=data, timeout=60)
    response.raise_for_status()
    payload = response.json()
    try:
        return payload["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError) as exc:
        raise ValueError(f"Unexpected Groq response: {payload}") from exc
