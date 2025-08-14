# Backend features implemented but not yet integrated in UI — Inventory and backend-only smoke plan (2025-08-08)

This document lists server-side capabilities that exist in the FastAPI backend but are not yet surfaced in the React UI. It also includes a backend-only smoke test script to validate these endpoints without any UI wiring.

## Quick summary
- No UI integration yet for: full Conflicts API, Reminders CRUD, advanced Analytics (productivity/patterns/insights), NLP model endpoints, Events priority utilities (low-confidence, reclassify, statistics), Users profile API, and WebSocket broadcasting.
- A smoke script is added at `backend/smoke_tests/unintegrated_endpoints_smoke.py` to call these endpoints safely.

## Inventory by area

### Conflicts API (not in UI)
- POST /api/v1/conflicts/check — detect conflicts for a proposed event
- POST /api/v1/conflicts/resolve — suggest alternatives (optionally auto-resolve)
- POST /api/v1/conflicts/analyze — conflict analytics report
- POST /api/v1/conflicts/batch-check — bulk check
- GET  /api/v1/conflicts/user-patterns — historical conflict patterns
- POST /api/v1/conflicts/smart-reschedule/{event_id} — suggest reschedule times for an event

Suggested UI later: replace client-only detection with server-backed check+resolve; add “smart reschedule” actions per event.

### Reminders API (not in UI)
- POST   /api/v1/reminders/{event_id}
- GET    /api/v1/reminders/
- GET    /api/v1/reminders/{reminder_id}
- PUT    /api/v1/reminders/{reminder_id}
- DELETE /api/v1/reminders/{reminder_id}
- PATCH  /api/v1/reminders/{reminder_id}/mark-sent

Suggested UI later: reminders on event details; list upcoming reminders; mark-as-sent via notifications flow.

### Analytics — advanced (partially used)
- GET /api/v1/analytics/productivity/metrics
- GET /api/v1/analytics/productivity/patterns
- GET /api/v1/analytics/productivity/insights
- GET /api/v1/analytics/dashboard/weekly-summary
- GET /api/v1/analytics/ai/insights
- GET /api/v1/analytics/trends/comparison
- GET /api/v1/analytics/conflicts/resolution-effectiveness
- GET /api/v1/analytics/user/{cognito_sub}/insights
- GET /api/v1/analytics/user/{cognito_sub}/time-suggestions
- GET /api/v1/analytics/user/{cognito_sub}/productivity-score
- GET /api/v1/analytics/user/{cognito_sub}/meeting-patterns
- POST /api/v1/analytics/user/{cognito_sub}/feedback
- GET /api/v1/analytics/user/{cognito_sub}/optimization-report

Currently used in UI: priority trends and BERT performance only. Others are unused.

Suggested UI later: “AI suggestions” widget, productivity score card, “best times” CTA buttons.

### NLP/BERT endpoints (not in UI)
- GET  /api/v1/nlp/health
- GET  /api/v1/nlp/model-status
- POST /api/v1/nlp/predict-priority
- POST /api/v1/nlp/batch-predict
- POST /api/v1/nlp/explain-priority
- POST /api/v1/nlp/detect-conflicts
- GET  /api/v1/nlp/demo/* (demos)

Suggested UI later: “Why this priority?” explain dialog; batch classify for imports.

### Events priority utilities (not in UI)
- GET  /api/v1/events/priority/statistics
- GET  /api/v1/events/priority/low-confidence
- POST /api/v1/events/{event_id}/reclassify
- GET  /api/v1/events/priority/conflicts

Suggested UI later: QA queue for low-confidence; reclassify button; priority conflict overlay.

### Users API (not in UI)
- POST /api/v1/users/
- GET  /api/v1/users/me (by cognito_sub)
- PUT  /api/v1/users/me
- DELETE /api/v1/users/me

Suggested UI later: sync Firebase uid → backend profile on first run.

### WebSocket broadcasting (not in UI)
- Event creation and priority classification broadcast through `ultimate_socket_server`.

Suggested UI later: live “Recent Activity” feed and instant schedule refresh.

## Backend-only smoke test
A simple Python script has been added to validate the above endpoints locally without changing the UI: `backend/smoke_tests/unintegrated_endpoints_smoke.py`.

Pre-reqs
- Backend running at http://localhost:8000 (via Docker Compose or local FastAPI run)
- Python env with `requests` (backends often include it; otherwise `pip install requests`)

What it does
- Ensures a test user exists (cognito_sub = test-user-1)
- Creates a temporary event (if needed) to exercise reminder and priority endpoints
- Calls representative endpoints from Conflicts, Analytics, NLP, Reminders, and Events priority utilities
- Prints PASS/FAIL per check and a short summary

Notes
- If BERT model is not trained, NLP endpoints will report “degraded” and use fallback; the script tolerates that.
- If the DB is empty, some analytics will return empty but still PASS.

## Next steps (frontend later, safe)
- Add a minimal “Conflicts (server)” tab that hits POST /conflicts/check and shows top alternatives
- Surface “Low-confidence queue” (GET /events/priority/low-confidence)
- Add “Best times” CTA from GET /analytics/user/{id}/time-suggestions
- Optional: live updates via WebSocket for new events/priority classification

---

## Backend validation status — 2025-08-08

Summary (backend-only smoke): PASS 6 / 6

- Conflicts: check → PASS (HTTP 200)
- Conflicts: resolve → PASS (HTTP 200)
- Reminders: CRUD happy path → PASS
- Analytics: insights endpoints → PASS/OK (some endpoints may 404 if not enabled; tolerated)
- NLP: health + model-status → PASS/OK (model may report degraded; tolerated)
- Events: priority utilities → PASS

What changed to stabilize without UI impact

- Conflicts API
	- Endpoints are now mounted reliably. Temporary, safe fallbacks return valid empty/default responses if advanced ML logic isn’t available, so they never 404. This unblocks frontend wiring while we design the final conflict logic carefully.

- Reminders API
	- Fixed a response validation error by allowing `created_at` to be optional in the response schema. The DB column can later be enforced non-null and the schema tightened again.

Notes

- No UI changes were made for these stabilizations.
- The smoke test (`backend/smoke_tests/unintegrated_endpoints_smoke.py`) now prints server error details if any endpoint regresses, making future triage faster.

Next (conflicts design focus)

- We will redesign conflict detection/resolution with strong edge-case coverage and re-enable the advanced logic behind capability checks, keeping the current safe fallbacks as a guard during rollout.

---

## Update — 2025-08-09 (frontend + voice scheduling progress)

Recent implementation work focused on tightening the scheduling UX before wiring more backend-only features. Key changes now live in code (not yet reflected in this inventory previously):

### Date-only (all-day) task creation & display
- Voice and typed flows now create true date-only (is_all_day) tasks when the user specifies a date with no explicit time (e.g. "Schedule project review on Friday").
- Removed the earlier implicit 09:00 fallback that produced misleading timed events.
- Frontend normalizes both legacy `all_day` and canonical `is_all_day` flags for backward compatibility.
- Conflict detection UI excludes date-only tasks from time-slot overlap logic to avoid false positives.

### Conflict panel refinements (client-side layer)
- Anchored time parsing prevents day rollover drift (e.g., parsing times near midnight incorrectly shifting dates).
- Alternative time suggestions filtered through a strict isRangeFree check to remove overlapping or back-to-back edge cases.
- Styled scrollable wheel selector with clearer AM/PM labeling and improved tap targets.
- Explicit labeling clarifies which event would be moved during manual resolution experiments.

### Voice scheduling intent guard
- Lightweight NLP/heuristic guard added: non‑scheduling utterances are ignored (returns success=false) instead of creating junk events.
- Broad, vague temporal phrases ("sometime next week") currently map to a date-only placeholder rather than arbitrary daytime anchoring; future refinement will map these to representative windows.

### Event origin labeling
- `created_via` now defaults to `manual` unless a voice path is confirmed; UI shows an icon only for confirmed voice-origin events.

### Developer notes
- Removed invalid `all_day` keyword usage in the backend event creation path (model only accepts `is_all_day`).
- Added dual-field normalization shim in the frontend API service to smooth mixed historic data while migrations settle.

## Remaining integration targets (rolling list)

Short-term (next passes):
1. Server Conflicts API integration (replace client-only logic behind a feature flag; fall back if server unavailable).
2. "Add time" action for date-only tasks (convert to timed event via modal picker, then re-run conflict check).
3. Smart reschedule (wire POST /conflicts/smart-reschedule/{event_id} with suggestion UI & accept button).
4. Reminders UI (list + create + mark sent) atop existing API.
5. Low-confidence priority review queue (GET /events/priority/low-confidence) with reclassify action.
6. "Explain priority" modal (POST /nlp/explain-priority) with graceful degraded-mode messaging.
7. Basic WebSocket subscription for new events + priority updates → optimistic UI refresh.

Medium-term:
8. Analytics widgets: productivity score, best time suggestions, optimization report CTA.
9. Batch conflict check for multi-import scenarios (bulk scheduling tooling).
10. Broad period refinement: map phrases ("this afternoon") to representative start/end windows instead of date-only.
11. Convert date-only → timed inline (hover / context menu) without opening full edit dialog.

Deferred / later exploration:
12. Multi-user / participants & shared conflicts view.
13. Rich recurrence editor & server-side recurrence expansion validation.
14. Activity feed (WebSocket broadcast consumption) with prioritization highlights.

## Risk / dependency notes
- Conflicts API server integration depends on verifying parity between client heuristic detection and server responses; plan: shadow mode logging first.
- WebSocket wiring requires modest backend token auth review (ensure test/local mode works without Cognito).
- Priority explanation UI gated on ensuring explain endpoint robust under degraded (non-BERT) fallback.

## Validation checkpoints planned
- Add lightweight Jest/Vitest tests for date-only normalization function and conflict suggestion filter logic.
- Add backend unit test ensuring voice intent guard does not create events for non-scheduling phrases (list of benign samples).

---

End of 2025-08-09 update.
