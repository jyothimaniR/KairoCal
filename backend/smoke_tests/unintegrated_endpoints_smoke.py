"""
Backend-only smoke test for unintegrated endpoints.

Enhancements:
- Auto-detects backend base URL (env KAIRO_BASE or KAIR0_BASE, then 8000, then 8001)
- Verifies DB tables exist, and will call /api/v1/database/create-tables if missing
- Safe and minimal writes (ensures a test user and a single event)
"""
import os
import sys
import time
from typing import Any, Dict, Tuple

import requests

# Base URL resolution: prefer KAIRO_BASE, fall back to legacy KAIR0_BASE, then probe 8000/8001
def resolve_base_url() -> Tuple[str, str]:
    import requests
    env_base = os.environ.get("KAIRO_BASE") or os.environ.get("KAIR0_BASE")
    candidates = [
        env_base,
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "http://localhost:8001",
        "http://127.0.0.1:8001",
    ]
    for base in [c for c in candidates if c]:
        try:
            r = requests.get(f"{base}/api/v1/status", timeout=2)
            if r.ok:
                return base, f"{base}/api/v1"
        except Exception:
            continue
    # Default
    return "http://localhost:8000", "http://localhost:8000/api/v1"

BASE, API = resolve_base_url()
USER = os.environ.get("KAIR0_USER", "test-user-1")  # maps to cognito_sub

summary: Dict[str, Any] = {"pass": [], "fail": []}

def check(name: str, func):
    try:
        func()
        print(f"PASS: {name}")
        summary["pass"].append(name)
    except Exception as e:
        print(f"FAIL: {name} -> {e}")
        summary["fail"].append((name, str(e)))

def ensure_tables():
    """Ensure required tables exist; create them if missing."""
    import requests
    try:
        r = requests.get(f"{API}/database/status", timeout=5)
        if r.ok:
            data = r.json()
            tables = set(data.get("tables", []))
            needed = {"users", "events", "reminders"}
            missing = needed - tables
            if missing:
                ct = requests.post(f"{API}/database/create-tables", timeout=10)
                ct.raise_for_status()
                print(f"Initialized DB tables: {ct.json().get('tables_created')}")
        else:
            r.raise_for_status()
    except Exception as e:
        # Non-fatal; continue, individual tests may fail with clearer errors
        print(f"WARN: database status/create-tables check failed: {e}")

def ensure_user():
    # create user profile if missing
    r = requests.get(f"{API}/users/me", params={"cognito_sub": USER})
    if r.status_code == 404:
        payload = {
            "cognito_sub": USER,
            "email": f"{USER}@example.com",
            "name": "Test User",
        }
        cr = requests.post(f"{API}/users/", json=payload)
        cr.raise_for_status()
    elif r.ok:
        pass
    else:
        r.raise_for_status()


def get_or_create_event() -> str:
    # list events; if none, create one
    r = requests.get(f"{API}/events", params={"cognito_sub": USER, "limit": 1})
    r.raise_for_status()
    data = r.json()
    if data:
        return data[0]["id"]
    from datetime import datetime, timedelta
    now = datetime.utcnow()
    payload = {
        "title": "Smoke Test Event",
        "description": "created by smoke test",
        "start_time": (now + timedelta(hours=2)).isoformat() + "Z",
        "end_time": (now + timedelta(hours=3)).isoformat() + "Z",
        "location": "Online",
    }
    cr = requests.post(
        f"{API}/events",
        params={"cognito_sub": USER, "auto_classify_priority": "true"},
        json=payload,
    )
    cr.raise_for_status()
    return cr.json()["id"]


def test_conflicts_check():
    from datetime import datetime, timedelta
    now = datetime.utcnow()
    payload = {
        "title": "Overlap Probe",
        "description": "probe",
        "start_time": (now + timedelta(hours=2)).isoformat() + "Z",
        "end_time": (now + timedelta(hours=3)).isoformat() + "Z",
        "buffer_minutes": 15,
    }
    r = requests.post(f"{API}/conflicts/check", params={"cognito_sub": USER}, json=payload)
    # 200 with [] or conflicts
    r.raise_for_status()


def test_conflicts_resolve():
    from datetime import datetime, timedelta
    now = datetime.utcnow()
    payload = {
        "title": "Resolve Probe",
        "start_time": (now + timedelta(hours=4)).isoformat() + "Z",
        "end_time": (now + timedelta(hours=5)).isoformat() + "Z",
        "buffer_minutes": 15,
    }
    r = requests.post(
        f"{API}/conflicts/resolve",
        params={"cognito_sub": USER, "auto_resolve": "false", "max_alternatives": 3},
        json=payload,
    )
    r.raise_for_status()


def test_reminders_flow(event_id: str):
    # create reminder
    payload = {"minutes_before": 30, "notification_type": "in_app"}
    cr = requests.post(f"{API}/reminders/{event_id}", params={"cognito_sub": USER}, json=payload)
    if not cr.ok:
        try:
            detail = cr.json()
        except Exception:
            detail = cr.text
        raise RuntimeError(f"create reminder failed: {cr.status_code} {detail}")
    rem = cr.json()
    rid = rem["id"]
    # list
    r = requests.get(f"{API}/reminders/", params={"cognito_sub": USER})
    r.raise_for_status()
    # mark sent
    ms = requests.patch(f"{API}/reminders/{rid}/mark-sent", params={"cognito_sub": USER})
    ms.raise_for_status()


def test_analytics_insights():
    for path in [
        "analytics/productivity/metrics",
        "analytics/productivity/patterns",
        "analytics/productivity/insights",
        "analytics/dashboard/weekly-summary",
        "analytics/ai/insights",
        "analytics/trends/comparison",
        "analytics/conflicts/resolution-effectiveness",
    ]:
        r = requests.get(f"{API}/{path}", params={"cognito_sub": USER})
        if r.status_code not in (200, 404):
            r.raise_for_status()


def test_nlp_status_and_predict():
    r = requests.get(f"{API}/nlp/health")
    r.raise_for_status()
    # Try model-status but tolerate 200 with degraded
    ms = requests.get(f"{API}/nlp/model-status")
    if ms.status_code not in (200, 503):
        ms.raise_for_status()


def test_events_priority_utils():
    for path in [
        "events/priority/statistics",
        "events/priority/low-confidence",
        "events/priority/conflicts",
    ]:
        r = requests.get(f"{API}/{path}", params={"cognito_sub": USER})
        if r.status_code not in (200, 404):
            r.raise_for_status()


if __name__ == "__main__":
    print("== KairoCal backend smoke for unintegrated endpoints ==")
    print(f"Base URL: {BASE}")
    try:
        ensure_tables()
        ensure_user()
        eid = get_or_create_event()
        check("Conflicts: check", test_conflicts_check)
        check("Conflicts: resolve", test_conflicts_resolve)
        check("Reminders: CRUD happy path", lambda: test_reminders_flow(eid))
        check("Analytics: insights endpoints", test_analytics_insights)
        check("NLP: status + model-status", test_nlp_status_and_predict)
        check("Events: priority utilities", test_events_priority_utils)
    finally:
        print("\nSummary:")
        print(f"  PASS: {len(summary['pass'])}")
        print(f"  FAIL: {len(summary['fail'])}")
        for name, err in summary["fail"]:
            print(f"   - {name}: {err}")
