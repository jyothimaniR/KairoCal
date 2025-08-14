# KairoCal Troubleshooting Guide

**Last Updated**: August 11, 2025  
**Version**: 1.0  

## Quick Reference

### Common Issues & Solutions

| Issue | Symptoms | Quick Fix |
|-------|----------|-----------|
| Voice API 404 | Voice endpoints return 404 | Check dependencies: `python-socketio`, `PyJWT` |
| Container Build Fails | Docker build errors | Use `--no-cache` flag |
| Import Errors | Module not found | Verify dependencies in `requirements/dev.txt` |
| Database Connection | 503 on /ready endpoint | Check PostgreSQL container status |
| BERT Model Loading | AI endpoints fail | Ensure adequate container memory |

## Voice API Issues

### Problem: Voice Endpoints Return 404 Errors

**Symptoms**:
- `GET /api/v1/voice/health` → 404 Not Found
- `POST /api/v1/voice/create-event` → 404 Not Found  
- Frontend voice features non-functional

**Diagnostic Steps**:

1. **Check Container Status**:
   ```bash
   docker ps
   # Verify kairocal_backend is running
   ```

2. **Test Direct Import**:
   ```bash
   docker exec kairocal_backend python -c "from app.api.voice import voice_router"
   ```

3. **Check Dependencies**:
   ```bash
   docker exec kairocal_backend pip list | grep -E "(socketio|JWT)"
   ```

**Common Root Causes**:
- Missing `python-socketio` dependency
- Missing `PyJWT` dependency  
- Silent import failure in try/catch block

**Resolution**:
1. Add missing dependencies to `backend/requirements/dev.txt`:
   ```
   python-socketio==5.7.2
   PyJWT==2.8.0
   ```

2. Rebuild container:
   ```bash
   docker compose down
   docker compose build --no-cache backend
   docker compose up -d
   ```

3. Verify fix:
   ```bash
   curl http://localhost:8000/api/v1/voice/health
   ```

### Problem: Voice Processing Fails

**Symptoms**:
- 200 response but `"success": false`
- Processing errors in response
- Missing NLP analysis

**Diagnostic Steps**:

1. **Check BERT Model Status**:
   ```bash
   curl http://localhost:8000/api/v1/voice/health
   # Look for "bert_model": "trained"
   ```

2. **Test Simple Voice Input**:
   ```bash
   curl -X POST http://localhost:8000/api/v1/voice/create-event \
     -H "Content-Type: application/json" \
     -d '{"voice_text": "test meeting", "user_id": "test-user"}'
   ```

3. **Check Container Resources**:
   ```bash
   docker stats kairocal_backend
   # Monitor memory usage during processing
   ```

## Database Issues

### Problem: Database Connection Failures

**Symptoms**:
- `/ready` endpoint returns 503
- SQLAlchemy connection errors
- Migration failures

**Diagnostic Steps**:

1. **Check PostgreSQL Container**:
   ```bash
   docker ps | grep postgres
   docker logs kairocal_postgres
   ```

2. **Test Database Connection**:
   ```bash
   docker exec kairocal_backend python -c "
   from app.core.database import engine
   with engine.connect() as conn:
       print('Database connection: OK')
   "
   ```

**Resolution**:
- Restart PostgreSQL container: `docker compose restart postgres`
- Check disk space: `df -h`
- Verify connection string in environment variables

### Problem: Migration Issues

**Symptoms**:
- Application won't start
- Database schema mismatches
- Alembic errors

**Diagnostic Steps**:

1. **Check Migration Status**:
   ```bash
   curl http://localhost:8000/api/v1/database/migration-status
   ```

2. **Run Migrations Manually**:
   ```bash
   docker exec kairocal_backend alembic upgrade head
   ```

**Resolution**:
- Reset database: `docker compose down -v && docker compose up -d`
- Check migration files for syntax errors
- Verify database permissions

## Docker Issues

### Problem: Container Build Failures

**Symptoms**:
- `docker compose build` fails
- Dependency installation errors
- Out of disk space

**Diagnostic Steps**:

1. **Check Available Space**:
   ```bash
   docker system df
   df -h
   ```

2. **Clean Docker Cache**:
   ```bash
   docker system prune -a
   ```

3. **Build with Verbose Output**:
   ```bash
   docker compose build --no-cache --progress=plain backend
   ```

**Resolution**:
- Use `--no-cache` for dependency changes
- Clean unused images and containers
- Increase disk space allocation

### Problem: Container Performance Issues

**Symptoms**:
- Slow API responses
- High memory usage
- Container restarts

**Diagnostic Steps**:

1. **Monitor Resources**:
   ```bash
   docker stats --no-stream
   ```

2. **Check Container Logs**:
   ```bash
   docker logs kairocal_backend --tail=100
   ```

**Resolution**:
- Increase container memory limits
- Optimize ML model loading
- Enable GPU acceleration if available

## API Issues

### Problem: 500 Internal Server Errors

**Symptoms**:
- Endpoints return 500
- Application errors
- Correlation ID in error response

**Diagnostic Steps**:

1. **Check Application Logs**:
   ```bash
   docker logs kairocal_backend | grep ERROR
   ```

2. **Use Correlation ID**:
   ```bash
   # Search logs for specific request ID
   docker logs kairocal_backend | grep "correlation-id-from-response"
   ```

3. **Test Health Endpoints**:
   ```bash
   curl http://localhost:8000/health
   curl http://localhost:8000/ready
   ```

**Resolution**:
- Check Python traceback in logs
- Verify request payload format
- Test with minimal valid request

### Problem: CORS Issues

**Symptoms**:
- Browser console CORS errors
- Cross-origin requests blocked
- OPTIONS requests failing

**Diagnostic Steps**:

1. **Check CORS Configuration**:
   ```bash
   # Look for CORS headers in response
   curl -v -H "Origin: http://localhost:3000" http://localhost:8000/health
   ```

2. **Verify Frontend URL**:
   - Check if frontend URL matches CORS origins in backend config

**Resolution**:
- Update CORS origins in FastAPI configuration
- Ensure proper HTTP methods allowed
- Check for wildcard vs specific origins

## NLP/ML Issues

### Problem: BERT Classification Failures

**Symptoms**:
- Low confidence scores
- No priority assigned
- BERT model errors

**Diagnostic Steps**:

1. **Check Model Status**:
   ```bash
   curl http://localhost:8000/api/v1/voice/health
   # Verify "bert_model": "trained"
   ```

2. **Test Simple Classification**:
   ```bash
   curl -X POST http://localhost:8000/api/v1/nlp/classify \
     -H "Content-Type: application/json" \
     -d '{"text": "urgent meeting tomorrow"}'
   ```

**Resolution**:
- Restart container to reload model
- Check model file integrity
- Verify adequate memory allocation

### Problem: Time Parsing Issues

**Symptoms**:
- Incorrect time extraction
- Timezone problems
- Date parsing errors

**Diagnostic Steps**:

1. **Test Temporal Resolver**:
   ```python
   from app.nlp.temporal_resolver import TemporalResolver
   resolver = TemporalResolver()
   result = resolver.resolve_time("tomorrow at 2 PM")
   print(result)
   ```

**Resolution**:
- Check timezone configuration
- Verify regex patterns in temporal resolver
- Test with various time formats

## Development Workflow Issues

### Problem: Hot Reload Not Working

**Symptoms**:
- Code changes not reflected
- Manual container restart needed
- Development slow

**Resolution**:
- Use volume mounts for development:
  ```yaml
  volumes:
    - ./backend:/app
  ```
- Ensure watchdog packages installed
- Check file permissions

### Problem: Environment Variables Not Loading

**Symptoms**:
- Default values used
- Configuration not applied
- Environment-specific behavior missing

**Resolution**:
- Check `.env` file location and format
- Verify environment variable names
- Use `docker-compose.override.yml` for local config

## Performance Optimization

### Memory Usage Optimization

1. **Monitor Memory**:
   ```bash
   docker stats kairocal_backend --no-stream
   ```

2. **Profile Application**:
   ```python
   import memory_profiler
   # Add @profile decorator to functions
   ```

3. **Optimize Model Loading**:
   - Use CPU-only models for development
   - Implement lazy loading
   - Cache model instances

### Response Time Optimization

1. **Enable Metrics**:
   ```bash
   curl http://localhost:8000/metrics
   ```

2. **Identify Slow Endpoints**:
   - Check logs for slow request warnings
   - Use profiling tools
   - Monitor database query times

3. **Optimization Strategies**:
   - Add caching layers
   - Optimize database queries
   - Use async processing for ML tasks

## Emergency Procedures

### Complete System Reset

```bash
# Stop all containers
docker compose down -v

# Clean Docker system
docker system prune -a

# Remove all volumes (⚠️ DATA LOSS)
docker volume prune

# Rebuild from scratch
docker compose build --no-cache
docker compose up -d
```

### Database Reset Only

```bash
# Stop backend (keep data safe)
docker compose stop backend

# Reset database
docker compose down postgres
docker volume rm kairocal_postgres_data

# Restart with fresh database
docker compose up -d
```

### Log Collection for Support

```bash
# Collect all relevant logs
mkdir debug-logs
docker logs kairocal_backend > debug-logs/backend.log
docker logs kairocal_postgres > debug-logs/postgres.log
docker logs kairocal_redis > debug-logs/redis.log
docker system info > debug-logs/system-info.txt
docker compose ps > debug-logs/container-status.txt
```

## Useful Commands Reference

### Docker Commands
```bash
# View running containers
docker ps

# View all containers (including stopped)
docker ps -a

# Check container logs
docker logs <container_name>

# Execute command in container
docker exec -it <container_name> bash

# Check container stats
docker stats <container_name>

# Rebuild specific service
docker compose build --no-cache <service_name>
```

### Database Commands
```bash
# Connect to PostgreSQL
docker exec -it kairocal_postgres psql -U kairocal -d kairocal

# Run migrations
docker exec kairocal_backend alembic upgrade head

# Check migration status
docker exec kairocal_backend alembic current

# Generate new migration
docker exec kairocal_backend alembic revision --autogenerate -m "description"
```

### API Testing Commands
```bash
# Health check
curl http://localhost:8000/health

# Readiness check  
curl http://localhost:8000/ready

# Voice health
curl http://localhost:8000/api/v1/voice/health

# Create voice event
curl -X POST http://localhost:8000/api/v1/voice/create-event \
  -H "Content-Type: application/json" \
  -d '{"voice_text": "test", "user_id": "test-user"}'
```

---

**Note**: This troubleshooting guide is based on real issues encountered during development. Update this document when new issues are discovered and resolved.
