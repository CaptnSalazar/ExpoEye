import os, requests, time
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
import uvicorn
from groq_client import call_groq
app = FastAPI(title='ExpoEye Orchestrator')
VISION_URL = os.getenv('VISION_AGENT_URL','http://localhost:8101/analyze')
CONTEXT_URL = os.getenv('CONTEXT_AGENT_URL','http://localhost:8102/enrich')

@app.post('/submit')
async def submit(image: UploadFile = File(...), note: str = Form(None)):
    files = {'file': (image.filename, await image.read(), image.content_type)}
    try:
        vis = requests.post(VISION_URL, files=files, timeout=20).json()
    except Exception as e:
        return JSONResponse({'error':f'vision error: {e}'},status_code=502)
    try:
        ctx = requests.post(CONTEXT_URL, json=vis, timeout=20).json()
    except Exception as e:
        return JSONResponse({'error':f'context error: {e}'},status_code=502)
    messages = [{'role':'system','content':'You are ExpoEye, concise assistant for expo attendees.'},
                {'role':'user','content':f"OCR: {vis['payload'].get('ocr_text','')}\nScene: {vis['payload'].get('scene')}\nHints: {ctx['payload'].get('hints')}\nUser note: {note or ''}"}]
    groq = call_groq(messages)
    final={'mcp_trace':{'vision':vis,'context':ctx,'groq_meta':groq.get('meta')},'advice':groq.get('text')}
    return JSONResponse(final)

if __name__=='__main__':
    uvicorn.run(app, host='0.0.0.0', port=int(os.getenv('ORCH_PORT',8200)))
