# Product development plan

Each round completes one feature or repair. Future items are planned, not implemented claims.

## Current round

skeleton

## Roadmap

### skeleton — FastAPI/React skeleton with install instructions and tests

Status: done

Acceptance:
- Backend FastAPI app starts and responds to /health
- Frontend Vite/React app builds and serves
- Docker compose brings up backend + frontend + Keycloak
- README has install/run/test steps
- pytest and vitest run without errors

Implementation: `backend/app/main.py`, `backend/requirements.txt`, `backend/Dockerfile`, `frontend/package.json`, `frontend/src/main.tsx`, `frontend/src/App.tsx`, `compose.yaml`, `README.md`, `.gitignore`, `.env.example`, `pyproject.toml`, `LICENSE`, `CHANGELOG.md`, `portfolio.json`

Tests: `backend/tests/test_health.py`, `frontend/src/__tests__/App.test.tsx`

### skill-catalog — Plugin/skill catalog with search and detail view

Status: in_progress

Acceptance:
- Backend stores plugins and skills in SQLite
- API supports pagination, filtering, search
- Frontend displays searchable catalog with detail view
- At least 3 workflows: browse, search, import from reference URL

Implementation: `backend/app/models/plugin.py`, `backend/app/schemas/plugin.py`, `backend/app/api/plugins.py`, `backend/app/db/init_db.py`, `backend/app/main.py`

Tests: `backend/tests/test_plugins.py`

### issue-tracker — GitHub issue ingestion and triage workflow

Status: planned

Acceptance:
- Backend fetches and stores issues from reference repo
- Frontend shows issue list with filtering by plugin/label
- AI-assisted triage suggestions (opt-in, labeled advisory)

### quality-analysis — Content quality analysis engine (Chinese anti-slop detection)

Status: planned

Acceptance:
- Deterministic offline analyzer for Chinese AI patterns
- API endpoint returns structured quality report
- Frontend workflow: paste text -> get quality score + suggestions

