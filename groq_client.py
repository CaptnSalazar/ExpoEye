"""groq_client.py
Wrapper for Groq / LLM API. Uses GROQ_API_KEY and GROQ_ENDPOINT environment variables.
If GROQ_API_KEY is 'demo' or empty, returns a deterministic mock response.
"""
import os, requests, time
from typing import List, Dict, Any

GROQ_API_KEY = os.getenv('GROQ_API_KEY','demo')
GROQ_ENDPOINT = os.getenv('GROQ_ENDPOINT','https://api.x.ai/v1/chat/completions')
DEFAULT_MODEL = os.getenv('GROQ_MODEL','grok-3-mini')

def _mock_response(messages: List[Dict[str,str]]):
    user = messages[-1].get('content','') if messages else ''
    return {'success': True, 'text': '[MOCK] Quick Groq-style reply: ' + (user[:300] + ('...' if len(user)>300 else '')), 'meta': {'mock': True}}

def call_groq(messages: List[Dict[str,str]], model: str = DEFAULT_MODEL, timeout: int = 12) -> Dict[str,Any]:
    if not GROQ_API_KEY or GROQ_API_KEY.lower()=='demo':
        return _mock_response(messages)
    headers = {'Authorization': f'Bearer {GROQ_API_KEY}', 'Content-Type': 'application/json'}
    payload = {'model': model, 'messages': messages, 'max_tokens': 300, 'temperature': 0.3}
    start = time.time()
    resp = requests.post(GROQ_ENDPOINT, headers=headers, json=payload, timeout=timeout)
    latency = time.time() - start
    if resp.status_code != 200:
        return {'success': False, 'text': f'[ERROR] Status {resp.status_code}: {resp.text[:200]}', 'meta': {'status': resp.status_code, 'latency': latency}}
    data = resp.json()
    try:
        text = data['choices'][0]['message']['content']
    except Exception:
        text = str(data)
    return {'success': True, 'text': text, 'meta': {'status': resp.status_code, 'latency': latency}}
