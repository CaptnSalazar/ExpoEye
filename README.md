# ExpoEye+ (Groq Integrated) — Consolidated Root Repo

This repository is the upgraded ExpoEye+ tailored to meet Groq Hackathon scoring: multi-agent architecture, MCP-style payloads, Groq integration, and benchmarking.

## What changed
- Real Groq client wrapper (groq_client.py) that uses GROQ_API_KEY and GROQ_ENDPOINT environment variables; falls back to deterministic mock when key is 'demo'.
- Vision, Context agents (FastAPI) and Orchestrator (FastAPI) calling Groq to generate final advice.
- Streamlit demo UI (app.py) posts images to orchestrator and displays MCP trace + advice.
- Dockerfile + docker-compose for local stack bring-up.
- benchmark.py for simple latency measurement.

## Quickstart (local demo)
1. Install system tesseract (OS-specific)
2. pip install -r requirements.txt
3. Start services (option A - simple)
   - Run vision: `python vision_agent.py`
   - Run context: `python context_agent.py`
   - Run orchestrator: `python orchestrator.py`
   - In a new shell: `streamlit run app.py`
4. Option B - Docker Compose
   - docker build -t expoeye .
   - docker-compose up --build
5. Run benchmark: `python benchmark.py`

## Environment Variables
- GROQ_API_KEY (set to 'demo' for mock mode)
- GROQ_ENDPOINT (defaults to https://api.x.ai/v1/chat/completions)
- VISION_AGENT_URL / CONTEXT_AGENT_URL / ORCH_URL to override defaults

## Submission checklist
- Include video demo link and live deployment if available.
- Provide commit SHA permalinks for app.py and orchestrator.py when submitting.
