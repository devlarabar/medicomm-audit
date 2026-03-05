# Clinical Communication Analyzer — Implementation Plan

## Overview

A lightweight FastAPI + single-page UI tool that analyzes doctor-patient
conversation logs through an AI pipeline, returning a structured report with
summary, risk analysis, quality scores, and safer rewrite suggestions.

Stack: Python, FastAPI, Anthropic Claude API, vanilla HTML/JS frontend.

---

## Phase 1: Project Scaffolding

### Commit 1: `Config: Init project directory structure`
**Files to create:**
- `app/__init__.py`
- `app/api/__init__.py`
- `app/ai_pipeline/__init__.py`
- `app/models/__init__.py`
- `frontend/.gitkeep`
- `logs/.gitkeep`

**What we're doing:**
- Create all package directories with empty `__init__.py` files
- Add placeholder files so empty dirs are tracked by git

---

### Commit 2: `Config: Add pyproject.toml for uv`
**Files to create:**
- `pyproject.toml`

**What we're doing:**
- Define project metadata and dependencies: `fastapi`, `uvicorn[standard]`,
  `anthropic`, `python-dotenv`
- uv will generate `uv.lock` on first `uv sync`

---

### Commit 3: `Feat: Bootstrap FastAPI app entry point`
**Files to create:**
- `app/main.py`

**What we're doing:**
- Initialize FastAPI app instance
- Add CORS middleware (allow all origins for local dev)
- Mount `frontend/` as static files
- Register API router

---

## Phase 2: Data Models

### Commit 4: `Feat: Define Pydantic schemas for pipeline I/O`
**Files to create:**
- `app/models/schemas.py`

**What we're doing:**
- `ConversationRequest` — `conversation: str`
- `RiskAnalysis` — `risk_types`, `severity`, `explanation`,
  `message_reference: int`, `safer_rewrite`
- `QualityScores` — four 0–100 int scores + `feedback: str`
- `FullReport` — composes all three above

---

## Phase 3: AI Pipeline

### Commit 5: `Feat: Add conversation summarizer module`
**Files to create:**
- `app/ai_pipeline/summarizer.py`

**What we're doing:**
- Accept `conversation_text: str`
- Prompt Claude to extract: symptoms, recommendations, medications,
  follow-up instructions
- Return plain summary string

---

### Commit 6: `Feat: Add risk analyzer module`
**Files to create:**
- `app/ai_pipeline/risk_analyzer.py`

**What we're doing:**
- Accept `conversation_text` and `summary`
- Prompt Claude to detect: unclear instructions, early medication stop,
  dismissed symptoms, missing follow-up, ambiguous advice
- Return structured JSON parsed into `RiskAnalysis`

---

### Commit 7: `Feat: Add communication quality scorer`
**Files to create:**
- `app/ai_pipeline/quality_scorer.py`

**What we're doing:**
- Accept `conversation_text` and `summary`
- Score clarity, empathy, safety, actionability (0–100 each)
- Return structured JSON parsed into `QualityScores`

---

### Commit 8: `Feat: Add report builder to assemble pipeline output`
**Files to create:**
- `app/ai_pipeline/report_builder.py`

**What we're doing:**
- Accept summary, risk, quality outputs
- Combine into a `FullReport` object
- No LLM calls — composition only

---

## Phase 4: API Route + Orchestrator

### Commit 9: `Feat: Add /analyze endpoint with pipeline orchestration`
**Files to create:**
- `app/api/routes.py`

**What we're doing:**
- `POST /analyze` accepts `ConversationRequest`
- Pipeline flow: `summarizer → risk_analyzer → quality_scorer → report_builder`
- Return `FullReport` as JSON response

---

## Phase 5: Frontend

### Commit 10: `Feat: Add single-page UI shell`
**Files to create:**
- `frontend/index.html`

**What we're doing:**
- Textarea for conversation input, "Analyze" button
- Placeholder result sections: Summary, Risk, Quality Scores, Rewrite
- Tailwind CSS via Play CDN (`<script src="https://cdn.tailwindcss.com">`)
- No build step required for the MVP

---

### Commit 11: `Feat: Add script.js to call API and render results`
**Files to create:**
- `frontend/script.js`

**What we're doing:**
- `fetch` POST to `/analyze`
- Populate each result section from response
- Loading state while in-flight, error message on failure

---

### Commit 12: `Feat: Pre-fill sample conversation for instant demo`
**Files to change:**
- `frontend/script.js`

**What we're doing:**
- Default textarea value: the antibiotic example from the spec
- Demo works without any typing

---

## Phase 6: Conversation Timeline Risk Markers

### Commit 13: `Feat: Add conversation message parser`
**Files to create:**
- `app/ai_pipeline/parser.py`

**What we're doing:**
- Parse raw text into list of `{index, speaker, text}` dicts
- Reused by risk analyzer and frontend

---

### Commit 14: `Feat: Update risk analyzer to return message index`
**Files to change:**
- `app/ai_pipeline/risk_analyzer.py`

**What we're doing:**
- Pass numbered messages to the prompt
- Prompt returns the exact message number where the risk occurs
- `message_reference` is now a reliable integer

---

### Commit 15: `Feat: Highlight risky message in frontend`
**Files to change:**
- `frontend/index.html`
- `frontend/script.js`

**What we're doing:**
- Render conversation as numbered list
- Highlight the message at `message_reference`
- Show "Risk detected in Message #N" indicator

---

## Phase 7: Multi-Conversation Metrics Dashboard

### Commit 16: `Feat: Add in-memory history store and /metrics endpoint`
**Files to change:**
- `app/api/routes.py`

**What we're doing:**
- Module-level `analysis_history = []` — append each report
- `GET /metrics` returns avg scores + total conversation count

---

### Commit 17: `Feat: Add metrics dashboard panel to frontend`
**Files to change:**
- `frontend/index.html`
- `frontend/script.js`

**What we're doing:**
- Fetch `/metrics` after each analysis
- Display live aggregate scores and total count

---

## Phase 8: Observability

### Commit 18: `Feat: Log pipeline stage output to logs/ directory`
**Files to change:**
- `app/ai_pipeline/summarizer.py`
- `app/ai_pipeline/risk_analyzer.py`
- `app/ai_pipeline/quality_scorer.py`

**What we're doing:**
- Write each stage's output to `logs/summary.json`, `logs/risk.json`,
  `logs/quality.json`
- Demonstrates AI observability and traceability

---

## Phase 9: Documentation

### Commit 19: `Docs: Add README with setup and architecture`
**Files to create:**
- `README.md`

**What we're doing:**
- What the tool does, who it's for
- ASCII architecture diagram
- Setup: `uv sync`, `.env` vars, `uv run uvicorn app.main:app --reload`
- Feature list

---

## Testing Strategy

- Manual test after each phase using the sample conversation
- After Phase 4: verify full API response with `curl`
- After Phase 5: open browser, confirm UI renders results correctly

## Rollback Plan

- Each commit is atomic — any single commit can be cleanly reverted
- No database, no migrations — stateless except in-memory history
- In-memory store resets on server restart (by design for MVP)

---

## Environment Variables Required

```
ANTHROPIC_API_KEY=...
```

Create a `.env` file (gitignored) before running.
