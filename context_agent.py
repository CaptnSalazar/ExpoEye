from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
import time
app = FastAPI(title='ExpoEye Context Agent')

CONF_DB = {'booths':{'42':{'name':'Tech Support Booth','help':'Debug & connectivity fixes'},'5':{'name':'Coffee Sponsor','help':'Free coffee'}},'schedule':[{'time':'10:30','room':'A','title':'AI Ethics'},{'time':'11:15','room':'B','title':'LLM Ops'}]}

class MCPPayload(BaseModel):
    mcp_version: str
    agent: str
    timestamp: float
    payload: Dict[str,Any]

@app.post('/enrich')
async def enrich(payload: MCPPayload):
    try:
        ocr = payload.payload.get('ocr_text','') or ''
    except Exception:
        raise HTTPException(status_code=400,detail='Malformed payload')
    hints=[]
    for b,v in CONF_DB['booths'].items():
        if b in ocr:
            hints.append({'type':'booth','id':b,'info':v})
    hints.append({'type':'schedule_snapshot','next_sessions':CONF_DB['schedule'][:2]})
    enriched={'mcp_version':'0.1','agent':'context_agent','timestamp':time.time(),'payload':{'original':payload.payload,'hints':hints,'confidence':0.9}}
    return enriched
