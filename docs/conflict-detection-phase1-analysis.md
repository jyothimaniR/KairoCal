# Conflict Detection — Phase 1 Analysis and Implementation Plan

## Scope and goals

This document captures an exhaustive analysis of the current conflict detection stack (backend + frontend) and outlines a pragmatic implementation plan to tighten backend/UX parity and ship smart, explainable rescheduling. This fulfills Phase 1: discovery and analysis, and provides a concrete multi-step plan to execute next.

## Requirements checklist

- Deep analysis of current conflict detection code and behavior — Done (backend + frontend)
- Identify quality/robustness gaps and mismatches — Done
- Propose a complete implementation plan for smart time slot recommendations — Done
- Keep changes low-risk and aligned with existing architecture — Planned in roadmap

## Current architecture (high-level)

- Backend (FastAPI):
  - Endpoints in `backend/app/api/conflicts.py` implement a safe “basic_v1” conflict engine using DB overlap with a ±15 min buffer.
  - Severity classification and simple nearest conflict-free alternatives (basic) are returned.
  - Smart-reschedule endpoint wires into `UserBehaviorAnalyzer.suggest_optimal_time_slots` and filters results by DB overlap for conflict-free assurance.
  - Batch check, analyze report, and user patterns endpoints exist.
  - An advanced `SmartConflictDetector` service integrates BERT-based priority inference; some sub-detectors (time/location/buffer/productivity) are placeholders.

- Frontend (React/TS):
  - `ConflictDetectionPanel.tsx` implements both client-side heuristic conflict detection and optional server-backed checks using `/api/v1/conflicts/*`.
  - It can reschedule events via `apiService.rescheduleEvent`, adjust priority, and call smart-reschedule to auto-apply the first alternative.
  - Drift logging compares client vs server results during a shadow window.
  - `DashboardPage.tsx` embeds the panel and shows productivity/AI status; priority alerts use client heuristics.
  - `apiService.ts` provides conflictsCheck/Resolve/SmartReschedule/events CRUD and analytics calls.

- Data model:
  - `Event` includes timing, location, and priority/analytics fields.
  - `User` includes preferences JSON for future per-user learning.

## Backend details observed

- Conflict checks rely on DB overlap with a safety buffer; timezone-naive vs aware issues are mitigated by tz stripping in handlers.
- Smart reschedule calls behavior analytics, then applies DB-overlap filtering to ensure alternatives are conflict-free before returning.
- Advanced detector has robust priority inference but several placeholder detectors, which is OK since the API uses basic_v1+analytics.

## Frontend details observed

- Client heuristic conflicts group events by identical start minute; this is simpler than backend overlap logic and can diverge in counts.
- Alternative time chips are hour-based and filtered client-side against the full events list to avoid overlaps.
- Smart-reschedule flow currently auto-applies the first alternative (no choice UI), then refreshes conflicts.
- Timezone concerns are partially handled via ISO strings; a custom parser avoids 1h drift in some locales.
- API feature flag `conflictsServerEnabled` supports shadow drift logging vs client heuristic.
- Safety checks in `apiService` guard eventId length (>32) for update/delete; could inadvertently reject valid IDs if formats change.

## Gaps and quality risks

- Detection parity: client groups by equal start time; backend detects true overlaps with buffers. This can produce drift and user confusion.
- Explainability: backend returns reasons only for smart-reschedule; UI does not yet surface reason stacks/confidence for multiple choices.
- Auto-apply behavior: smart-reschedule picks the first server alternative without showing options; users can’t compare choices.
- ID validation: front-end checks eventId length < 32 → false may reject valid non-UUID formats or shorter dev IDs.
- Timezone: multiple conversions across client/server could still yield edge drift for DST or locale parsing; mitigation exists but should be validated.

## Implementation plan (incremental, low risk)

1) Parity and stability
   - Prefer server detection results when available, but surface a small “computed by server” badge to set expectations.
   - Keep client heuristic as fallback; log parity drift in background only.
   - Soften eventId guards: accept canonical UUID (36) and any non-empty string; rely on API error response rather than length checks.

2) Smart-reschedule UX
   - Replace auto-apply with a compact selection modal that lists top 3–5 server suggestions:
     - Show start/end, a confidence bar, and conflict risk badge (Low/Med/High) + a short “Why this time?” reason.
     - Allow “Use this time” → calls reschedule API.
     - If no server suggestions, gracefully fall back to local hour chips.

3) Backend enhancements (targeted)
   - Enrich `UserBehaviorAnalyzer` scoring explanations (reason stack) and include numeric confidence on each alternative.
   - Ensure `/conflicts/smart-reschedule/{event_id}` returns: start_time, end_time, confidence (0–1), conflict_risk (‘Low’|‘Medium’|‘High’), reasons: string[].
   - Keep DB-overlap filter as last check before returning suggestions.

4) New suggestions API (optional but recommended)
   - Add `POST /api/v1/suggestions` for new-event planning (duration, preferred_date, title/desc optional) returning N ranked slots with reasons/confidence.
   - Wire to `UserBehaviorAnalyzer` with the same overlap filtering.

5) Telemetry and online learning (phase 2)
   - Add a lightweight endpoint to record suggestion acceptance/rejection; update per-user hour/day weights in `User.preferences`.
   - Fold these weights back into scoring as multipliers (bounded 0–1), improving personalization over time.

6) Validation
   - Add unit tests for analyzer scoring and API schemas (happy path + boundary: no events, dense calendar, all-day events).
   - UI smoke: reschedule modal opens, shows suggestions, accepts one, and updates the UI.
   - Parity: small script compares client heuristic vs server results on a seeded dataset; log discrepancies.

## Suggested UX changes (frontend)

- ConflictDetectionPanel
  - Add a “Smart alternatives” modal list when server suggestions are present.
  - Render per-option: label, confidence bar, risk badge, tooltip with reason stack.
  - Keep current quick hour chips as fallback with local overlap check.

- DashboardPage
  - No structural changes required; the panel remains embedded.

## Notes on timezones

- Continue emitting ISO UTC to the backend and normalizing server-side. Avoid string-local parsing on the client when constructing API payloads.
- Keep the custom parser for AM/PM labels anchored to a specific date to avoid DST surprises.

## Risk and mitigation

- Divergence between client/server conflict counts: show server badge and use server results when available; keep drift logs for diagnostics.
- Over-automation: replacing auto-apply with a choice list reduces surprises and increases trust with reasons/confidence.
- Backward compatibility: maintain current endpoints and types; add fields rather than breaking changes.

## Deliverables and sequencing

- D1–D2: Backend suggestion reason/confidence + response schema; frontend modal and wiring; relax eventId guard.
- D3: Optional `/api/v1/suggestions` for new-event planning and QuickScheduler integration.
- D4: Tests and parity check harness; finalize docs.

## Quality gates (current state)

- Build: N/A (analysis-only doc)
- Lint/Typecheck: No changes to code yet
- Unit tests: N/A (plan includes adding tests in next phase)

## Requirements coverage

- Analysis of conflict detection codebase: Done
- Identify gaps and propose fixes: Done
- Plan for smart time slot recommendations and UI: Done
- Keep changes low-risk and incremental: Planned (see Deliverables and sequencing)
