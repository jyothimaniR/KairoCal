"""Lightweight in‑process metrics collection for FastAPI & DB.

Provides:
  - HTTP request counters & duration aggregation per method+path_template+status
  - Slow request counter (threshold configurable via SLOW_REQUEST_THRESHOLD_MS)
  - DB query counters & slow query tracking (threshold via SLOW_QUERY_THRESHOLD_MS)
  - Export in Prometheus text exposition format at /metrics

This is intentionally minimal (no histograms) to avoid extra deps. Can be
swapped for prometheus_client later without touching app code if we keep a
small facade of increment/observe functions.
"""
from __future__ import annotations
import threading, time, hashlib
from typing import Tuple
from collections import defaultdict

_lock = threading.Lock()

# HTTP metrics: key = (method, path_template, status)
_http_counts = defaultdict(int)  # type: ignore[var-annotated]
_http_durations_sum = defaultdict(float)  # key=(method,path)
_http_durations_count = defaultdict(int)
_http_durations_max = defaultdict(float)
_http_slow_requests = 0

# DB metrics
_db_total_queries = 0
_db_slow_queries = 0
_db_query_samples = defaultdict(int)

def record_http_request(method: str, path_template: str, status: int, duration_ms: float, slow_threshold_ms: int):
    global _http_slow_requests
    key = (method, path_template, str(status))
    dur_key = (method, path_template)
    with _lock:
        _http_counts[key] += 1
        _http_durations_sum[dur_key] += duration_ms
        _http_durations_count[dur_key] += 1
        if duration_ms > _http_durations_max[dur_key]:
            _http_durations_max[dur_key] = duration_ms
        if duration_ms >= slow_threshold_ms:
            _http_slow_requests += 1

def record_db_query(sql: str, duration_ms: float, slow_threshold_ms: int):
    global _db_total_queries, _db_slow_queries
    with _lock:
        _db_total_queries += 1
        if duration_ms >= slow_threshold_ms:
            _db_slow_queries += 1
            normalized = " ".join(sql.strip().split())[:500]
            h = hashlib.sha1(normalized.encode()).hexdigest()[:12]
            _db_query_samples[h] += 1

def render_prometheus() -> str:
    lines = []
    lines.append('# HELP http_requests_total Total HTTP requests')
    lines.append('# TYPE http_requests_total counter')
    with _lock:
        for (method, path, status), count in sorted(_http_counts.items()):
            lines.append(f'http_requests_total{{method="{method}",path="{path}",status="{status}"}} {count}')
        lines.append('# HELP http_request_duration_ms_sum Cumulative request duration in ms')
        lines.append('# TYPE http_request_duration_ms_sum counter')
        for (method, path), total_ms in sorted(_http_durations_sum.items()):
            lines.append(f'http_request_duration_ms_sum{{method="{method}",path="{path}"}} {total_ms:.3f}')
        lines.append('# HELP http_request_duration_ms_count Number of timed HTTP requests')
        lines.append('# TYPE http_request_duration_ms_count counter')
        for (method, path), cnt in sorted(_http_durations_count.items()):
            lines.append(f'http_request_duration_ms_count{{method="{method}",path="{path}"}} {cnt}')
        lines.append('# HELP http_request_duration_ms_max Max observed request duration in ms')
        lines.append('# TYPE http_request_duration_ms_max gauge')
        for (method, path), max_ms in sorted(_http_durations_max.items()):
            lines.append(f'http_request_duration_ms_max{{method="{method}",path="{path}"}} {max_ms:.3f}')
        lines.append('# HELP http_slow_requests_total Requests slower than threshold')
        lines.append('# TYPE http_slow_requests_total counter')
        lines.append(f'http_slow_requests_total {_http_slow_requests}')
        lines.append('# HELP db_queries_total Total DB queries executed')
        lines.append('# TYPE db_queries_total counter')
        lines.append(f'db_queries_total {_db_total_queries}')
        lines.append('# HELP db_slow_queries_total DB queries slower than threshold')
        lines.append('# TYPE db_slow_queries_total counter')
        lines.append(f'db_slow_queries_total {_db_slow_queries}')
        if _db_query_samples:
            lines.append('# HELP db_slow_query_fingerprint_total Slow query fingerprints (top counts)')
            lines.append('# TYPE db_slow_query_fingerprint_total counter')
            for h, c in sorted(_db_query_samples.items(), key=lambda x: -x[1])[:50]:
                lines.append(f'db_slow_query_fingerprint_total{{fingerprint="{h}"}} {c}')
    return "\n".join(lines) + "\n"
