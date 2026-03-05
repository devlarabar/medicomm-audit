# Concise LLM Responses Implementation Plan

## Overview
Tighten the system prompts and max_tokens across quality scoring, risk analysis, and
summarization to cut output length by ~50%.

## Commits (in order)

### Commit 1: refactor: tighten LLM prompts and token limits for ~50% shorter responses

**Files to change:**
- app/ai_pipeline/summarizer.py
- app/ai_pipeline/risk_analyzer.py
- app/ai_pipeline/quality_scorer.py

**What we're doing:**

summarizer.py:
- Add "Keep the total summary under 150 words." to system prompt
- Reduce max_tokens: 1024 → 512

risk_analyzer.py:
- Change `explanation` field description to "one sentence max"
- Change `safer_rewrite` description to "concise rephrasing only, one sentence"
- Reduce max_tokens: 2048 → 1024

quality_scorer.py:
- Change `feedback` description from "2-3 sentences" to "1 sentence"
- Reduce max_tokens: 1024 → 512

**Why:**
- Prompts currently allow verbose responses with no hard length constraints
- Halving max_tokens enforces the ceiling at the API level
- Explicit word/sentence limits in the prompt guide the model before it generates

## Testing Strategy
- Run the pipeline against an existing test conversation and compare output lengths
- Verify JSON structure is preserved for risk and quality (no schema breaks)

## Rollback Plan
- Revert the commit; all changes are isolated to three prompt strings and three
  integer literals
