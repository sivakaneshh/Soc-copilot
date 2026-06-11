import os
from pathlib import Path
from typing import Any, Dict, List, Optional

import requests
from dotenv import load_dotenv


_DOTENV_PATH = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(_DOTENV_PATH if _DOTENV_PATH.exists() else None)

HF_TOKEN = os.getenv("HF_TOKEN")
HF_MODEL_ID = os.getenv("HF_MODEL_ID", "EQuIP-Queries/EQuIP_3B")
HF_FALLBACK_MODEL_ID = os.getenv("HF_FALLBACK_MODEL_ID", "meta-llama/Llama-3.1-8B-Instruct")
HF_API = "https://router.huggingface.co/v1/chat/completions"
HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"} if HF_TOKEN else {}


def _format_hit(hit: Dict[str, Any]) -> str:
    source = hit.get("_source", {}) or {}
    timestamp = source.get("@timestamp") or source.get("timestamp") or "unknown time"
    message = source.get("message") or "No message available"
    fields = []

    for key in ["user", "source_ip", "dest_ip", "host", "log_type", "severity", "event_type", "status"]:
        value = source.get(key)
        if value:
            fields.append(f"{key}={value}")

    field_text = f" ({', '.join(fields)})" if fields else ""
    return f"- {timestamp}: {message}{field_text}"


def format_search_hits(search_result: Dict[str, Any], max_hits: int = 5) -> List[str]:
    hits = search_result.get("hits", {}).get("hits", []) if isinstance(search_result, dict) else []
    return [_format_hit(hit) for hit in hits[:max_hits]]


def build_rag_prompt(question: str, search_result: Dict[str, Any], intent: Optional[str] = None) -> str:
    context_lines = format_search_hits(search_result)
    context_block = "\n".join(context_lines) if context_lines else "- No relevant log entries were returned."

    intent_line = f"Intent: {intent}\n" if intent else ""
    return (
        "You are SOC Copilot, a security analyst assistant. Answer the user using only the provided log evidence. "
        "If the evidence is insufficient, say so clearly and suggest what to look at next. Keep the answer concise and practical.\n\n"
        f"{intent_line}"
        f"Question: {question}\n\n"
        f"Retrieved log evidence:\n{context_block}\n\n"
        "Response format:\n"
        "- One short answer paragraph\n"
        "- Then 2-4 bullet points with key evidence or next steps"
    )


def _request_chat_completion(prompt: str, model_id: str, max_tokens: int, timeout: int) -> str:
    payload = {
        "model": model_id,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are SOC Copilot, a security analyst assistant. Answer using only the provided log evidence. "
                    "If the evidence is insufficient, say so clearly and suggest what to look at next. Keep the answer concise and practical."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        "max_tokens": max_tokens,
        "stream": False,
    }
    resp = requests.post(HF_API, headers=HEADERS, json=payload, timeout=timeout)
    try:
        data = resp.json()
    except Exception:
        data = resp.text

    if not resp.ok:
        if isinstance(data, dict):
            error_value = data.get("error")
            if isinstance(error_value, dict):
                error_message = error_value.get("message") or str(error_value)
            else:
                error_message = str(error_value)
        else:
            error_message = str(data)
        raise RuntimeError(error_message or f"HTTP {resp.status_code}")

    if isinstance(data, dict):
        choices = data.get("choices")
        if isinstance(choices, list) and choices:
            first_choice = choices[0] or {}
            message = first_choice.get("message") or {}
            content = message.get("content")
            if isinstance(content, str) and content.strip():
                return content
        if "error" in data:
            error_value = data.get("error")
            if isinstance(error_value, dict):
                error_message = error_value.get("message") or str(error_value)
            else:
                error_message = str(error_value)
            return f"[hf_error] {error_message}"

    return f"[hf_error] Unexpected Hugging Face response: {data}"


def generate_answer(prompt: str, max_tokens: int = 256, timeout: int = 30) -> str:
    try:
        return _request_chat_completion(prompt, HF_MODEL_ID, max_tokens=max_tokens, timeout=timeout)
    except Exception as primary_error:
        primary_message = str(primary_error)
        if "model_not_supported" not in primary_message and "provider" not in primary_message.lower():
            return f"[hf_error] {primary_message}"

        try:
            return _request_chat_completion(prompt, HF_FALLBACK_MODEL_ID, max_tokens=max_tokens, timeout=timeout)
        except Exception as fallback_error:
            return f"[hf_error] {fallback_error}"


def generate_rag_answer(
    question: str,
    search_result: Dict[str, Any],
    intent: Optional[str] = None,
    max_tokens: int = 256,
    timeout: int = 30,
) -> str:
    context_lines = format_search_hits(search_result)
    if not context_lines:
        return "I could not find relevant log evidence for that query. Try a narrower time range or a more specific host, user, or IP address."

    prompt = build_rag_prompt(question, search_result, intent=intent)
    def _synthesize_from_evidence(question: str, context_lines: List[str]) -> str:
        # Build a concise fallback answer using the retrieved evidence
        top = context_lines[:3]
        short = f"Found {len(context_lines)} relevant log entries. Top findings: {'; '.join(top)}"
        bullets = [
            "- Review the top-listed log entries for affected users and IPs.",
            "- Consider investigating the hosts and blocking suspicious IPs if confirmed.",
        ]
        return short + "\n\n" + "\n".join(bullets)

    if not HF_TOKEN:
        return _synthesize_from_evidence(question, context_lines)

    answer = generate_answer(prompt, max_tokens=max_tokens, timeout=timeout)
    if answer.startswith("[hf_error]"):
        return _synthesize_from_evidence(question, context_lines)

    return answer