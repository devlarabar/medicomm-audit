# UI Redesign Implementation Plan

## Overview
Replace the single-column scrolling layout with a full-screen dashboard.
No page scroll — each panel scrolls internally. All content visible at once.

## Commits (in order)

### Commit 1: feat: redesign UI as full-screen dashboard layout

**Files to change:**
- frontend/index.html
- frontend/script.js

**What we're doing:**

index.html:
- `body`: `h-screen overflow-hidden flex flex-col`
- Add 48px header bar with logo icon + title/subtitle
- Left panel (320px, white, border-right): textarea fills height, Analyze
  button pinned to bottom
- Right panel (flex-1): three rows
  - Row 1 (flex-shrink-0): Summary card, full width
  - Row 2 (flex-shrink-0): Quality + Metrics side by side
  - Row 3 (flex-1, min-h-0): Timeline | Risks side by side, each scrollable
- Empty state (shown before first analysis): centered icon + text

script.js:
- On results render: hide `#empty-state`, add `flex` class to `#results`
- On metrics panel show: add `flex` class alongside removing `hidden`
- `renderTimeline`: compact list items, monospace index numbers
- `renderRisks`: tighter cards, risk tags before explanation
- `renderQuality` / metrics: same score bar template, unified helper

**Why:**
- Current layout requires scrolling past input to see results
- Full viewport layout lets clinicians see all panels simultaneously
- Internal scroll on timeline/risks keeps long content accessible

## Testing Strategy
- Open in browser, verify layout fills viewport without page scroll
- Run an analysis and verify all panels populate correctly
- Resize window to check panels remain usable

## Rollback Plan
- Single commit; revert it to restore the previous layout
