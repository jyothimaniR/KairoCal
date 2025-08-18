# Smart Conflict Detection Debugging Guide

## Current Issue: Server Mode Shows Only 1 Conflict Instead of 4 Expected

This guide provides systematic debugging steps for the Smart Conflict Detection system when it's not detecting the expected number of conflicts.

---

## Issue Analysis

### Expected Behavior
- User creates event that should conflict with 4 existing events
- BERT-powered conflict detection should identify all 4 conflicts
- Frontend should display comprehensive conflict analysis

### Actual Behavior
- Server mode detects only 1 conflict instead of 4
- BERT system appears functional but incomplete detection

---

## Debugging Checklist

### 1. Database Query Issues

**Check All-Day Event Filtering**
```sql
-- Verify which events are marked as all-day
SELECT id, title, is_all_day, start_time, end_time 
FROM events 
WHERE user_id = [USER_ID] 
ORDER BY start_time;
```

**Problem**: All-day events are excluded from time-specific conflict detection
**Location**: `backend/app/api/conflicts.py` line 120
```python
Event.is_all_day == False,  # 🔧 FIX: Only check non-all-day events
```

**Solution**: Ensure expected conflicting events have `is_all_day = False`

### 2. Self-Conflict Exclusion

**Check for Identical Events**
```python
# Self-conflict exclusion logic in conflicts.py line 124-128
~(
    (Event.start_time == req_start) & 
    (Event.end_time == req_end) & 
    (Event.title == conflict_request.title)
)
```

**Problem**: Events with identical time and title are excluded
**Debugging**: Verify proposed event doesn't match existing events exactly

### 3. Timezone Handling

**Check Timezone Consistency**
```python
# Debug timezone information
print(f"🔍 Request timezone: {conflict_request.start_time.tzinfo}")
print(f"🔍 Database timezone: {existing_event.start_time.tzinfo}")

# Normalization to naive UTC
def _naive(dt: datetime) -> datetime:
    return dt.replace(tzinfo=None)
```

**Problem**: Timezone-aware vs naive datetime comparison issues
**Solution**: All datetimes are normalized to naive UTC for comparison

### 4. Buffer Time Configuration

**Check Buffer Impact**
```python
buf = conflict_request.buffer_minutes or 0
start = req_start - timedelta(minutes=buf)
end = req_end + timedelta(minutes=buf)
```

**Debugging Steps**:
1. Test with `buffer_minutes: 0` to check raw overlaps
2. Test with `buffer_minutes: 15` (default) to verify buffer logic
3. Compare results to identify buffer-related exclusions

### 5. Overlap Detection Logic

**Core Overlap Query**
```python
overlapping = db.query(Event).filter(
    Event.user_id == user.id,
    Event.is_all_day == False,
    Event.start_time < end_q,    # Event starts before new event ends
    Event.end_time > start_q,    # Event ends after new event starts
    # Exclude self-conflicts
).all()
```

**Manual Verification**:
```python
# Add debug logging to see what's found
print(f"🔍 DEBUG: Query range: {start_q} to {end_q}")
all_events = db.query(Event).filter(Event.user_id == user.id).all()
print(f"🔍 DEBUG: All user events ({len(all_events)}):")
for ev in all_events:
    print(f"   - {ev.title}: is_all_day={ev.is_all_day}, start={ev.start_time}, end={ev.end_time}")
```

---

## Debugging Tools

### 1. Enable Debug Logging

**Add to conflicts.py** (already present):
```python
print(f"🔍 DEBUG: Checking conflicts for user {user.id}")
print(f"🔍 DEBUG: Query range: {start_q} to {end_q}")
print(f"🔍 DEBUG: Overlapping non-all-day events found: {len(overlapping)}")
for ev in overlapping:
    print(f"   - CONFLICT: {ev.title} ({ev.start_time} to {ev.end_time})")
```

### 2. Database Inspection Queries

**View All User Events**:
```sql
SELECT 
    id, title, start_time, end_time, is_all_day, location,
    EXTRACT(DOW FROM start_time) as day_of_week,
    EXTRACT(HOUR FROM start_time) as start_hour
FROM events 
WHERE user_id = [USER_ID]
ORDER BY start_time;
```

**Check Specific Overlap**:
```sql
-- Replace with actual test event times
SELECT 
    id, title, start_time, end_time, is_all_day,
    (start_time < '2025-01-27 15:00:00') as starts_before_end,
    (end_time > '2025-01-27 14:00:00') as ends_after_start
FROM events 
WHERE user_id = [USER_ID]
    AND is_all_day = FALSE
    AND start_time < '2025-01-27 15:00:00'  -- New event end
    AND end_time > '2025-01-27 14:00:00'    -- New event start
ORDER BY start_time;
```

### 3. API Testing

**Test Conflict Detection Directly**:
```bash
curl -X POST "http://localhost:8000/api/v1/conflicts/check" \
-H "Content-Type: application/json" \
-d '{
  "cognito_sub": "USER_SUB_ID",
  "conflict_request": {
    "title": "Test Meeting",
    "description": "Test conflict detection",
    "start_time": "2025-01-27T14:00:00Z",
    "end_time": "2025-01-27T15:00:00Z",
    "location": "Office",
    "is_all_day": false,
    "buffer_minutes": 0
  },
  "engine": "basic_v1"
}'
```

**Check Model Status**:
```bash
curl -X GET "http://localhost:8000/api/v1/nlp/model-status"
curl -X GET "http://localhost:8000/api/v1/nlp/health"
```

### 4. Frontend Debugging

**Check API Response in Browser Console**:
```javascript
// In ConflictDetectionPanel.tsx
const detectConflicts = async () => {
  console.log('🔍 Sending conflict check request:', eventData);
  const conflicts = await apiService.conflictsCheck(cognito_sub, eventData, "basic_v1");
  console.log('🔍 Raw API response:', conflicts);
  const mappedConflicts = mapServerResponseToDetected(conflicts);
  console.log('🔍 Mapped conflicts:', mappedConflicts);
  setDetectedConflicts(mappedConflicts);
};
```

---

## Common Root Causes & Solutions

### 1. All-Day Event Interference

**Problem**: Expected conflicting events are marked as `is_all_day = true`
**Solution**: 
- Update test data to set `is_all_day = false` for time-specific events
- Or modify query logic to handle all-day conflicts appropriately

### 2. Exact Time Matches

**Problem**: Proposed event has identical time/title as existing event
**Solution**: 
- Modify test data to have different titles
- Adjust time by a few minutes to avoid exact matches

### 3. Buffer Window Issues

**Problem**: Buffer time excludes expected conflicts
**Testing**:
```python
# Test scenarios
scenarios = [
    {"buffer": 0, "description": "No buffer - raw overlaps only"},
    {"buffer": 15, "description": "15min buffer - default setting"},
    {"buffer": 30, "description": "30min buffer - extended window"}
]
```

### 4. Database Timezone Inconsistency

**Problem**: Mixed timezone storage causing comparison failures
**Solution**:
- Verify all events stored with consistent timezone
- Check application timezone configuration
- Ensure frontend sends timezone-aware datetime strings

### 5. BERT Model Issues

**Problem**: BERT classifier not functioning properly
**Debugging**:
```python
# Test BERT functionality
try:
    smart_detector = SmartConflictDetector(db)
    priority, confidence = smart_detector._infer_event_priority_enhanced(test_event)
    print(f"BERT Priority: {priority}, Confidence: {confidence}")
except Exception as e:
    print(f"BERT Error: {e}")
```

---

## Step-by-Step Debugging Process

### Phase 1: Data Verification
1. Query database to list all user events
2. Verify expected conflicting events exist
3. Check `is_all_day` flags on all events
4. Confirm timezone consistency

### Phase 2: Query Logic Testing
1. Test conflict detection with `buffer_minutes: 0`
2. Add debug logging to see query results
3. Manually verify overlap logic with sample data
4. Check self-conflict exclusion logic

### Phase 3: BERT Integration Testing
1. Verify BERT models are loaded (`/api/v1/nlp/model-status`)
2. Test priority classification directly (`/api/v1/nlp/predict-priority`)
3. Check SmartConflictDetector initialization
4. Verify fallback mechanisms work

### Phase 4: End-to-End Testing
1. Test via API directly (curl/Postman)
2. Test via frontend with browser console logging
3. Compare expected vs actual results
4. Document findings and apply fixes

### Phase 5: Validation
1. Create controlled test scenarios
2. Verify all 4 expected conflicts are detected
3. Test edge cases (all-day events, exact matches, buffers)
4. Confirm BERT analysis is included in responses

---

## Expected Debug Output

When working correctly, you should see:
```
🔍 DEBUG: Checking conflicts for user 12345
🔍 DEBUG: Query range: 2025-01-27 13:45:00 to 2025-01-27 15:15:00
🔍 DEBUG: All user events (8):
   - Morning Standup: is_all_day=False, start=2025-01-27 09:00:00, end=2025-01-27 09:30:00
   - Client Call: is_all_day=False, start=2025-01-27 14:00:00, end=2025-01-27 14:30:00
   - Team Meeting: is_all_day=False, start=2025-01-27 14:30:00, end=2025-01-27 15:30:00
   - Project Review: is_all_day=False, start=2025-01-27 15:00:00, end=2025-01-27 16:00:00
   - Lunch Break: is_all_day=False, start=2025-01-27 12:00:00, end=2025-01-27 13:00:00
🔍 DEBUG: Overlapping non-all-day events found: 4
   - CONFLICT: Client Call (2025-01-27 14:00:00 to 2025-01-27 14:30:00)
   - CONFLICT: Team Meeting (2025-01-27 14:30:00 to 2025-01-27 15:30:00)
   - CONFLICT: Project Review (2025-01-27 15:00:00 to 2025-01-27 16:00:00)
   - CONFLICT: Another Meeting (2025-01-27 14:15:00 to 2025-01-27 14:45:00)
```

---

## Quick Fixes to Try

### 1. Remove Buffer Temporarily
```javascript
// In frontend, test with no buffer
const testEventData = {
  ...eventData,
  buffer_minutes: 0
};
```

### 2. Check Raw Database Results
```python
# Add this to conflicts.py for debugging
print("🔍 RAW QUERY RESULTS:")
raw_overlaps = db.query(Event).filter(
    Event.user_id == user.id,
    Event.start_time < end_q,
    Event.end_time > start_q,
).all()
for ev in raw_overlaps:
    print(f"   - RAW: {ev.title} (all_day={ev.is_all_day})")
```

### 3. Test Direct API Call
```bash
# Replace with your actual user and event data
curl -X POST "http://localhost:8000/api/v1/conflicts/check" \
  -H "Content-Type: application/json" \
  -d @test_conflict_request.json
```

This debugging guide should help identify why the BERT-powered Smart Conflict Detection system is only finding 1 conflict instead of the expected 4 conflicts.
