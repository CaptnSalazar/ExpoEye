"""groq_client.py
Light wrapper to call Groq / LLM backend. Uses mock mode when GROQ_API_KEY=demo.
"""
import os
import requests
from typing import Dict, Any

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "demo")
GROQ_ENDPOINT = os.getenv("GROQ_ENDPOINT", "https://api.x.ai/v1/chat/completions")  # placeholder

def call_groq(messages: list, model: str = "grok-3-mini", timeout: int = 15) -> Dict[str, Any]:
    """
    messages: list of {role, content}
    returns dict: {success, text, meta}
    """
    if GROQ_API_KEY in ("", "demo", None):
        combined = " | ".join([m.get("content","") for m in messages[-2:]])
        return {"success": True, "text": f"[MOCK] Groq reply for: {combined}", "meta": {"model": model, "mock": True}}
    try:
        headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
        payload = {"model": model, "messages": messages, "max_tokens": 300}
        resp = requests.post(GROQ_ENDPOINT, headers=headers, json=payload, timeout=timeout)
        resp.raise_for_status()
        data = resp.json()
        text = data["choices"][0]["message"]["content"]
        return {"success": True, "text": text, "meta": {"status_code": resp.status_code}}
    except Exception as e:
        return {"success": False, "text": f"[ERROR] {e}", "meta": {"error": str(e)}}
