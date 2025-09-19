"""orchestrator.py
FastAPI Orchestrator: routes image to vision agent, calls context agent, then Groq client for final advice.
"""
import os, requests, time
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
import uvicorn

from groq_client import call_groq

app = FastAPI(title='ExpoEye Orchestrator')

VISION_AGENT_URL = os.getenv('VISION_AGENT_URL', 'http://localhost:8101/analyze')
CONTEXT_AGENT_URL = os.getenv('CONTEXT_AGENT_URL', 'http://localhost:8102/enrich')

@app.post('/submit')
async def submit(image: UploadFile = File(...), note: str = Form(None)):
    files = {'file': (image.filename, await image.read(), image.content_type)}
    try:
        vis = requests.post(VISION_AGENT_URL, files=files, timeout=20).json()
    except Exception as e:
        return JSONResponse({'error': f'Vision agent error: {e}'}, status_code=502)
    try:
        ctx = requests.post(CONTEXT_AGENT_URL, json=vis, timeout=20).json()
    except Exception as e:
        return JSONResponse({'error': f'Context agent error: {e}'}, status_code=502)

    messages = [
        {'role': 'system', 'content': 'You are ExpoEye, a succinct assistant for expo attendees.'},
        {'role': 'user', 'content': f"Image OCR: {vis['payload'].get('ocr_text','')}\nScene: {vis['payload'].get('scene')}\nHints: {ctx['payload'].get('hints')}\nUser note: {note or ''}"}
    ]
    groq_resp = call_groq(messages)
    final = {
        'mcp_trace': {
            'vision': vis,
            'context': ctx,
            'groq_meta': groq_resp.get('meta')
        },
        'advice': groq_resp.get('text')
    }
    return JSONResponse(final)

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=int(os.getenv('ORCH_PORT', 8200)))
