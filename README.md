# ExpoEye+ Consolidated Submission

This repository contains a consolidated, root-level codebase for the ExpoEye+ multi-agent system tailored for the Groq/MachineHack hackathon requirements.

Included components (all at repo root):
- app.py (Streamlit demo UI that runs a local orchestrator in-process)
- vision_agent.py (FastAPI image analysis agent)
- context_agent.py (FastAPI context enrichment agent)
- groq_client.py (wrapper for Groq LLM calls — mock when GROQ_API_KEY=demo)
- orchestrator.py (FastAPI orchestrator combining agents and calling Groq)
- benchmark.py (simple latency benchmark)
- Dockerfile & docker-compose.yml for containerized local testing
- index.html (landing page)
- demo_images/ placeholders (not included inside ZIP binary; ensure you add images before running)

## Quick start (demo UI)
```bash
pip install -r requirements.txt
streamlit run app.py
```
For full multi-service run (Docker):
```bash
docker build -t expoeye+ .
docker-compose up --build
# then run benchmark.py
python benchmark.py
```

## Notes
- Tesseract system package must be installed for OCR to work.
- Groq integration is mockable; set GROQ_API_KEY env var to enable real calls.
- All services live at repo root as requested.

See ARCHITECTURE.png for a visual diagram (included).
