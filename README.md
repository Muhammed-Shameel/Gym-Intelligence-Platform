# Gym & Fitness Intelligence Platform (GFIP)

GFIP is a Phase 1 agentic AI application for gym member engagement, retention monitoring, trainer allocation, follow-up review, and auditable decision support.

The project includes a FastAPI backend, SQLAlchemy domain models, deterministic rule agents, LangGraph orchestration, controlled LLM-assisted summary generation, and a polished React dashboard/workflow console.

## Current Status

Production-ready Phase 1 demo foundation.

Included:

- FastAPI service layer with health, member, trainer, workflow, and audit endpoints.
- SQLite-backed sample data seeding for local demos.
- SQLAlchemy domain models for members, trainers, attendance, memberships, follow-up activity, and audits.
- Deterministic agents for attendance, engagement, trainer allocation, follow-up, and summary support.
- LangGraph workflow orchestration with route-aware execution.
- LLM-assisted explanation node with schema validation and deterministic fallback.
- React/Vite frontend with dashboard analytics, member detail pages, workflow console, admin view, and responsive UI polish.
- Human-readable final decision summaries with separated actions, explanation text, and audit reference.

## Application Highlights

- **Dashboard analytics:** Shows member totals, active/inactive status, join trends, popular training tags, and recent member activity.
- **Member detail console:** Displays member profile information, clearly visible Section ID, status, join date, and training tags.
- **Agent workflow console:** Runs the engagement workflow and shows conditional routing, engagement overview, final decision support, and audit metadata.
- **Readable decision output:** Final recommendations are rendered as action tiles with a clean explanation block instead of raw model/provider text.
- **Governed LLM behavior:** LLM output is limited to narrative explanation drafting. Core recommendations, routes, and protected fields remain deterministic and validated.
- **Fallback safe:** If the LLM path is disabled, unavailable, malformed, or fails validation, the system falls back to deterministic explanation output.

## Project Structure

```text
backend/
  app/
    api/                 FastAPI routers
    application/llm/      LLM prompt, provider, schema, validation, fallback logic
    core/                Settings and database setup
    data/                Seed/import helpers and sample data
    models/              SQLAlchemy domain models
    services/            Context builder, agents, rules, orchestrators
  tests/                 Backend verification tests

frontend/
  src/
    api/                 Frontend API client
    components/          App layout
    pages/               Dashboard, members, detail, workflow, admin, showcase
    styles.css           Shared UI system and responsive polish
    types/               Frontend TypeScript types
```

## Local Backend

From the repository root:

```bash
cd backend
python -m venv ..\.venv
..\.venv\Scripts\activate
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

Open:

- `http://localhost:5173`

The frontend expects:

```env
VITE_API_BASE_URL=http://localhost:8000
```

## Environment Variables

Backend `.env` values:

```env
DATABASE_URL=sqlite:///./gfip.db
CORS_ORIGINS=http://localhost:5173
LLM_ENABLED=true
LLM_PROVIDER=mock
LLM_MODEL=mock-agentic-v1
LLM_API_KEY=
GEMINI_API_KEY=
```

Use `LLM_PROVIDER=gemini` with a valid key only when testing Gemini-backed explanation drafting. Do not commit real API keys.

## Docker

```bash
docker compose up --build
```

Frontend:

- `http://localhost:8080`

Backend:

- `http://localhost:8000`

## Verification

Backend tests:

```bash
cd backend
pytest
```

Frontend production build:

```bash
cd frontend
npm run build
```

Optional end-to-end demo check:

1. Start the backend on port `8000`.
2. Start the frontend on port `5173`.
3. Open the dashboard and confirm member analytics render.
4. Open a member profile and confirm the Section ID is visible.
5. Run the workflow console and confirm the final decision summary is readable.
6. Confirm the audit reference is displayed.

## Safety And Scope

- Demo data is fictional.
- The system does not implement medical, injury, nutrition, or protected-attribute scoring.
- LLM output is not allowed to alter protected deterministic workflow fields.
- Recommendation logic should remain deterministic and auditable.
- UI polish should preserve existing workflows, API behavior, data models, and route structure.

## Phase 1 Sequence

1. Product, domain, and architecture readiness.
2. Application foundation and domain data.
3. Context builder and shared workflow context.
4. Deterministic agents and rule engine.
5. LangGraph orchestration, recommendation, and audit.
6. Controlled LLM explanation node with validation and fallback.
7. Dashboard, workflow console, UI polish, and final handover.
