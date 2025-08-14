# Database (PostgreSQL Only)
The project now uses **only PostgreSQL** (SQLite fallback removed to avoid drift and connectivity confusion).
Connect:
```bash
docker exec -it kairocal_postgres psql -U kairocal_user -d kairocal
```

Key endpoints for database health:
| Endpoint | Purpose |
|----------|---------|
| `GET /ready` | Readiness (fails if migration out-of-sync) |
| `GET /api/v1/database/status` | Tables + migration info |
| `GET /api/v1/database/migration-status` | Raw migration status (ok/pending/diverged) |

Environment variables controlling DB startup:
| Var | Default (dev) | Description |
|-----|---------------|-------------|
| `DATABASE_URL` | postgresql://... | Connection string (required) |
| `AUTO_MIGRATE` | true (dev) | Auto run Alembic upgrade on startup |
| `READINESS_REQUIRE_MIGRATION_SYNC` | true | If true, readiness blocks until schema matches head |
| `STATEMENT_TIMEOUT_MS` | 5000 | Per-connection statement timeout |
| `DB_POOL_SIZE` | 10 | SQLAlchemy pool size |
| `DB_MAX_OVERFLOW` | 5 | Extra connections allowed |

Removed:
* `USE_SQLITE_DEV` and SQLite fallback
* `/api/v1/database/create-tables` endpoint (replaced by migrations only)

Migration flow (dev):
```bash
alembic revision --autogenerate -m "describe change"
alembic upgrade head
```

If `/ready` returns 503 with `migration_status=pending`, run the upgrade command above.

## Observability (Phase 2 Enhancements)

Lightweight in‑process instrumentation (no external deps) has been added:

| Endpoint | Purpose |
|----------|---------|
| `GET /metrics` | Prometheus text exposition (scrape target) |

### Metrics Exposed

HTTP Request Metrics:
* `http_requests_total{method,path,status}` – counter
* `http_request_duration_ms_sum{method,path}` and `_count` – cumulative latency
* `http_request_duration_ms_max{method,path}` – max observed latency
* `http_slow_requests_total` – requests exceeding threshold

Database Metrics:
* `db_queries_total` – total SQL statements executed
* `db_slow_queries_total` – queries slower than threshold
* `db_slow_query_fingerprint_total{fingerprint}` – counts of slow query fingerprints (top 50)

### Slow Thresholds (env vars)
| Var | Default | Meaning |
|-----|---------|---------|
| `SLOW_REQUEST_THRESHOLD_MS` | 500 | Requests >= this are counted/logged as slow |
| `SLOW_QUERY_THRESHOLD_MS` | 200 | Queries >= this are counted/logged as slow |

### Structured Logging Additions
Slow queries emit: `{ event:"slow_query", duration_ms, sql }` (abbreviated SQL)
Slow requests emit standard warning log: `SLOW_REQUEST <METHOD> <ms> <path>`

### Prometheus Scrape Example (k8s ServiceMonitor)
```yaml
endpoints:
   - port: http
      path: /metrics
      interval: 15s
```

For production, consider swapping the in‑process collector for `prometheus_client` histogram buckets for latency SLO tracking.
# KairoCal: AI-Powered Smart Calendar

An intelligent, cloud-native calendar application that processes natural language input to create and manage events automatically.

## 🚀 Features

- **Natural Language Processing**: Create events using voice or text input
- **Smart Scheduling**: Intelligent conflict detection and resolution
- **Cloud-Native**: Built on AWS with modern DevOps practices
- **Responsive UI**: Modern React interface with Tailwind CSS
- **Secure Authentication**: AWS Cognito integration

## 🏗️ Architecture

- **Frontend**: React 18 + Vite + Tailwind CSS
- **Backend**: FastAPI + SQLAlchemy + PostgreSQL
- **NLP**: Hugging Face Transformers + spaCy
- **Cloud**: AWS (EKS, RDS, S3, CloudFront, Cognito)
- **DevOps**: Docker + Terraform + GitHub Actions

## 🛠️ Quick Start

1. **Setup Environment**
   ```bash
   make setup
   ```

2. **Run Development Servers**
   ```bash
   # Terminal 1 - Backend
   make dev-backend
   
   # Terminal 2 - Frontend  
   make dev-frontend
   ```

3. **Run Tests**
   ```bash
   make test
   ```

## 📁 Project Structure

```
kairocal/
├── backend/           # FastAPI application
├── frontend/          # React application
├── infrastructure/    # Terraform & K8s configs
├── docs/             # Documentation
└── scripts/          # Utility scripts
```

## 📚 Documentation

- [Technical Architecture](docs/architecture/README.md)
- [API Documentation](docs/api/openapi.yaml)
- [Deployment Guide](docs/deployment/README.md)
- [User Guide](docs/user-guide/README.md)

## 🧪 Testing

- Backend: pytest with 70%+ coverage
- Frontend: Jest + React Testing Library
- Integration: Postman collections
- E2E: Cypress (coming soon)

## 🚀 Deployment

## 🐳 Docker / Development Environment

Official development stack uses a single compose file: `docker-compose.yml`.

What it provides:
- `backend` (FastAPI + full ML/NLP dependencies from `requirements/dev.txt`)
- `postgres` (primary database)
- `redis` (caching / realtime support)

Removed / consolidated:
- `docker-compose-simple.yml` (DB-only) and `docker-compose.bert-training.yml` were eliminated to reduce confusion. Use the main stack; for specialized training runs, invoke scripts inside the running backend container or add a temporary service in a feature branch.

Image build now installs full dependencies (torch, transformers, numpy, socket.io, analytics libs) so the OpenAPI spec reflects ALL endpoints without stubs or feature gating. A legacy lightweight mode remains available for spec generation: `python backend/scripts/validate_openapi.py --light-mode`.

OpenAPI Contract:
```
docker compose up -d --build
docker exec -it kairocal_backend python scripts/validate_openapi.py --fail-on-diff
```
Snapshot stored at `backend/scripts/openapi_snapshot.json`.

Virtualenv Note:
Previously a host-created `backend/venv` (Windows) was mounted but unusable inside Linux containers. The repo now ignores and removes that directory; container installs dependencies globally within the image layer for reproducibility.

## 🔍 Backend Unification & OpenAPI Snapshot (August 2025)

This section documents the recent consolidation work so future contributors (or automated agents) understand decisions and state.

### Goals
* Single authoritative Docker image with FULL ML/NLP stack (no stubs, no feature flags required for normal operation).
* Deterministic OpenAPI contract tracked in git for drift detection.
* Remove obsolete compose variants and broken Windows virtualenv artifacts.
* Resolve dependency conflicts blocking reproducible builds.

### Key Changes
| Area | Change | Rationale |
|------|--------|-----------|
| Dockerfile | Switched to install `requirements/dev.txt` (full deps) | Ensures spec generation includes analytics / conflicts / NLP endpoints |
| Dependencies | Removed duplicate `python-dateutil` and extra `spacy` entries; added `email-validator` | Fixed build resolver error & Pydantic EmailStr import failure |
| OpenAPI Validation | Simplified `scripts/validate_openapi.py`; removed stub injections; added optional `--light-mode` | Cleaner CI and accurate default spec |
| Snapshot | Added `backend/scripts/openapi_snapshot.json` and whitelisted in `.gitignore` | Drift detection & reviewable API changes |
| Compose | Removed obsolete `version:` key and legacy compose files | Eliminated warnings & confusion |
| Virtualenv | Deleted stale `backend/venv` + ignored it | Prevent cross‑platform breakage |
| Pydantic Warnings | Added `protected_namespaces` in settings Config | Suppressed cosmetic `model_` field warnings |

### OpenAPI Snapshot Lifecycle
1. Generate/update: `docker compose exec backend python scripts/validate_openapi.py` (updates snapshot if no `--fail-on-diff`).
2. Enforce in CI: `python backend/scripts/validate_openapi.py --fail-on-diff` (fails if spec drift).
3. Intentional spec change workflow:
   - Make code change.
   - Run validation without `--fail-on-diff` locally to update snapshot.
   - Commit snapshot in same PR with rationale in commit message.

### Current Spec Stats
* Paths: 53
* Snapshot size: ~135 KB (JSON, normalized + sorted keys)
* Feature Groups Included: core events, reminders, conflicts, analytics, NLP/BERT, health, database status.

### Common Failure Modes & Fixes
| Symptom | Cause | Fix |
|---------|-------|-----|
| Build fails with `ResolutionImpossible` (dateutil) | Conflicting pinned versions | Ensure single entry (2.9.0.post0) in `dev.txt` |
| `ERROR: email-validator is not installed` | Missing dependency for Pydantic `EmailStr` | Add `email-validator` to `dev.txt` |
| Large diff on first full run | Previous snapshot was minimal | Accept & commit new snapshot (review additions) |
| Pydantic protected namespace warnings (`model_*`) | Default reserved prefix | Config `protected_namespaces = ("settings_",)` or rename fields |
| Snapshot not added to git | Caught by `*.json` ignore rule | Add `!backend/scripts/openapi_snapshot.json` to `.gitignore` |

### Recommended CI Step (add to workflow)
```bash
python backend/scripts/validate_openapi.py --fail-on-diff
```

### Future Optimizations
* Consider CPU-only torch build if GPU acceleration not required (reduces image size significantly).
* Add pre-commit hook running spec validation + formatting.
* Introduce contract test verifying selected critical endpoints (e.g. conflicts, NLP predict) remain stable.
* Auto-generate markdown summary from snapshot for docs (`docs/api/README.md`).

### Recent Commit Timeline (most recent first)
| Commit | Summary |
|--------|---------|
| `0323941` | Fix: move protected_namespaces into Config to resolve Pydantic error |
| `7a490e9` | Chore: remove obsolete compose version key; suppress model_ warnings |
| `78e3c15` | Track OpenAPI snapshot; adjust .gitignore |
| `3a8f171` | Unify backend: add email-validator; rebuild; update snapshot |

---
This log should be extended (append only) if further structural backend or API contract changes are made.


The application is deployed on AWS using:
- **EKS**: Container orchestration
- **RDS**: PostgreSQL database
- **S3 + CloudFront**: Static file hosting
- **Cognito**: User authentication

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Jyothi Mani Ravi Sankar**  
Master's Dissertation Project  
University of Liverpool  
Department of Computer Science
