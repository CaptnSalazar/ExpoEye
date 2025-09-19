"""context_agent.py
FastAPI Context Agent: accepts MCP payload from vision agent and returns enriched context.
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
import uvicorn, time, os

app = FastAPI(title='ExpoEye Context Agent')

CONF_DB = {
    'booths': {
        '42': {'name': 'Tech Support Booth', 'help': 'Debug & connectivity fixes'},
        '5': {'name': 'Coffee Sponsor', 'help': 'Free coffee'}
    },
    'schedule': [
        {'time': '10:30', 'room': 'Hall A', 'title': 'AI Ethics Panel'},
        {'time': '11:15', 'room': 'Hall B', 'title': 'LLM Ops'}
    ],
    'speakers': {'Jane Doe': {'bio': 'Works on responsible ML'}}
}

class MCPPayload(BaseModel):
    mcp_version: str
    agent: str
    timestamp: float
    payload: Dict[str, Any]

@app.post('/enrich')
async def enrich(payload: MCPPayload):
    try:
        ocr_text = payload.payload.get('ocr_text', '') or ''
        scene = payload.payload.get('scene', '') or ''
    except Exception:
        raise HTTPException(status_code=400, detail='Malformed payload')

    hints = []
    for b in CONF_DB['booths']:
        if b in ocr_text:
            hints.append({'type': 'booth', 'id': b, 'info': CONF_DB['booths'][b]})
    hints.append({'type': 'schedule_snapshot', 'next_sessions': CONF_DB['schedule'][:2]})

    enriched = {
        'mcp_version': '0.1',
        'agent': 'context_agent',
        'timestamp': time.time(),
        'payload': {
            'original': payload.payload,
            'hints': hints,
            'confidence': 0.9
        }
    }
    return enriched

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=int(os.getenv('CONTEXT_AGENT_PORT', 8102)))
