# Gym & Fitness Intelligence Platform (GFIP)

## Repository

`RealRails-AgenticAI-GFIP-Phase1`

## Current Status

Phase 1 foundation complete: Context Builder, Deterministic Agent Framework, Rule Engine, Orchestration, and Audit API implemented.

Included:

- FastAPI
- SQLAlchemy
- ...
- Context Builder
- Deterministic Agents
- Rule engine
- Orchestrator
- Final recommendation
- Audit retrieval

Not included:

- LangGraph
- LLM

## Local Backend

```bash
cd backend
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python -m app.data.seed
uvicorn app.main:app --reload --port 8000
```

Open:

- `http://localhost:8000/health`
- `http://localhost:8000/docs`

## Local Frontend

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173`.

## Docker

```bash
docker compose up --build
```

## Tests

```bash
cd backend
pytest
```

## Phase 1 Sequence

1. Product, Domain and Architecture Readiness
2. Application Foundation and Domain Data
3. Context Builder and Shared Workflow Context
4. Deterministic Agents and Rule Engine
5. Orchestration, Recommendation and Audit
6. Dashboard, Validation and Handover

## Safety

Use fictional demo data. Do not implement medical, injury, nutrition, or protected-attribute scoring.
