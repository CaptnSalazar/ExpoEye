# Architecture

ExpoEye+ multi-agent architecture (root-level files for quick run).

mermaid code (render in GitHub):
```mermaid
flowchart TB
  User --> Orchestrator[Orchestrator (root)]
  Orchestrator --> Vision[vision_agent.py]
  Vision --> Orchestrator
  Orchestrator --> Context[context_agent.py]
  Orchestrator --> Groq[groq_client.py]
  Groq --> Orchestrator
  Orchestrator --> UserResult[Final Advice]
```
