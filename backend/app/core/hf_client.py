import os
import requests
from typing import Optional

HF_TOKEN = os.getenv("HF_TOKEN")
HF_MODEL_ID = os.getenv("HF_MODEL_ID", "EQuIP-Queries/EQuIP_3B")
HF_API = f"https://api-inference.huggingface.co/models/{HF_MODEL_ID}"
HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"} if HF_TOKEN else {}

def generate_answer(prompt: str, max_tokens: int = 256, timeout: int = 30) -> str:
    payload = {
        "inputs": prompt,
        "parameters": {"max_new_tokens": max_tokens, "return_full_text": False}
    }
    try:
        resp = requests.post(HF_API, headers=HEADERS, json=payload, timeout=timeout)
        resp.raise_for_status()
        data = resp.json()
        # Typical HF inference returns a list of dicts with 'generated_text'
        if isinstance(data, list) and isinstance(data[0], dict) and "generated_text" in data[0]:
            return data[0]["generated_text"]
        if isinstance(data, dict) and "generated_text" in data:
            return data["generated_text"]
        if isinstance(data, list) and isinstance(data[0], str):
            return data[0]
        return str(data)
    except Exception as e:
        return f"[hf_error] {str(e)}"