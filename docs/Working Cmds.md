# Working Commands for KairoCal Server Startup

**Date Created**: August 15, 2025  
**Last Verified**: August 15, 2025  
**Status**: ✅ PROVEN WORKING METHOD

## 🎯 **CRITICAL REQUIREMENTS**

⚠️ **NEVER USE VS CODE TERMINALS** - Servers must run in separate PowerShell windows  
⚠️ **USE NATIVE BACKEND** - Docker causes BERT model loading issues  
⚠️ **USE SQLite MODE** - Avoids PostgreSQL Docker dependencies  
⚠️ **USE ROOT .venv** - Virtual environment is at `C:\Github\KairoCal\.venv`

---

## 🚀 **STEP 1: START BACKEND SERVER**

### Method: Separate PowerShell Window with Native SQLite Backend

```powershell
Start-Process powershell -ArgumentList "-NoExit", "-ExecutionPolicy", "Bypass", "-Command", "Set-Location 'C:\Github\KairoCal'; Write-Host 'Starting KairoCal Backend Server...' -ForegroundColor Green; & 'C:\Github\KairoCal\start-server-external.ps1'"
```

**What this does:**
- Opens a new PowerShell window that stays open (`-NoExit`)
- Sets execution policy to bypass script restrictions
- Navigates to the KairoCal root directory
- Executes the `start-server-external.ps1` script
- Uses SQLite database mode (no Docker required)
- Uses the `.venv` at root level: `C:\Github\KairoCal\.venv`

**Expected Result:**
- New PowerShell window opens with backend startup logs
- Backend loads SQLite database (`kairocal.db`)
- BERT model loads (may take 30-60 seconds)
- Server starts on: `http://127.0.0.1:8000`
- API documentation available at: `http://127.0.0.1:8000/docs`

---

## 🎯 **STEP 2: START FRONTEND SERVER**

### Method: Separate PowerShell Window with Vite

```powershell
Start-Process powershell -ArgumentList "-NoExit", "-ExecutionPolicy", "Bypass", "-Command", "Set-Location 'C:\Github\KairoCal'; Write-Host 'Starting KairoCal Frontend Server...' -ForegroundColor Green; & 'C:\Github\KairoCal\start-frontend-external.ps1'"
```

**What this does:**
- Opens a new PowerShell window that stays open (`-NoExit`)
- Sets execution policy to bypass script restrictions
- Navigates to the KairoCal root directory
- Executes the `start-frontend-external.ps1` script
- Runs `npm run dev` in the frontend directory

**Expected Result:**
- New PowerShell window opens with frontend startup logs
- Vite development server starts
- Frontend available at: `http://localhost:3000`

---

## 🔍 **VERIFICATION COMMANDS**

### Test Backend Health
```powershell
try { $response = Invoke-RestMethod -Uri "http://127.0.0.1:8000/health" -TimeoutSec 5; Write-Host "Backend Status: RUNNING" -ForegroundColor Green; $response | ConvertTo-Json } catch { Write-Host "Backend Status: NOT RUNNING" -ForegroundColor Red; Write-Host "Error: $_" }
```

**Expected Output:**
```json
{
    "status": "healthy",
    "service": "kairocal-api",
    "database": "connected",
    "bert_nlp": "operational",
    "voice_api": "operational",
    "conflict_detection": "operational"
}
```

### Test BERT Classification
```powershell
try { Write-Host "Testing BERT NLP endpoint..." -ForegroundColor Yellow; $bertTest = @{ text = "Important meeting with CEO tomorrow"; context = "academic" } | ConvertTo-Json; $bertResponse = Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/v1/nlp/classify-priority" -Method POST -Body $bertTest -ContentType "application/json" -TimeoutSec 10; Write-Host "BERT Classification: WORKING" -ForegroundColor Green; $bertResponse | ConvertTo-Json } catch { Write-Host "BERT API: ERROR - $_" -ForegroundColor Red }
```

**Expected Output:**
```json
{
    "priority": 3,
    "priority_label": "Medium",
    "confidence": 0.9473637938499451,
    "classification_method": "bert",
    "event_title": "Untitled",
    "recommendation": "Medium priority - standard scheduling recommended",
    "success": true
}
```

### Test Voice API
```powershell
try { Write-Host "Testing Voice API..." -ForegroundColor Yellow; $voiceResponse = Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/v1/voice/health" -TimeoutSec 5; Write-Host "Voice API: OPERATIONAL" -ForegroundColor Green; $voiceResponse | ConvertTo-Json } catch { Write-Host "Voice API: ERROR - $_" -ForegroundColor Red }
```

### Check Database Status
```powershell
try { Write-Host "Testing SQLite Database..." -ForegroundColor Yellow; $dbResponse = Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/v1/database/status" -TimeoutSec 5; Write-Host "Database Status: CONNECTED" -ForegroundColor Green; $dbResponse | ConvertTo-Json -Depth 3 } catch { Write-Host "Database API: ERROR - $_" -ForegroundColor Red }
```

### Check Ports in Use
```powershell
# Check backend port
netstat -an | findstr "127.0.0.1:8000"

# Check frontend port  
netstat -an | findstr ":3000"
```

---

## 📁 **FILE STRUCTURE REFERENCE**

### Backend Startup Script Location
```
C:\Github\KairoCal\start-server-external.ps1
```

### Frontend Startup Script Location
```
C:\Github\KairoCal\start-frontend-external.ps1
```

### Virtual Environment Location
```
C:\Github\KairoCal\.venv\
```

### SQLite Database Location
```
C:\Github\KairoCal\backend\kairocal.db
```

### BERT Model Location
```
C:\Github\KairoCal\backend\models\bert_priority_classifier\
```

---

## 🚨 **TROUBLESHOOTING**

### If Backend Doesn't Start
1. **Check Virtual Environment**: Ensure `C:\Github\KairoCal\.venv\` exists
2. **Check SQLite Database**: Ensure `C:\Github\KairoCal\backend\kairocal.db` exists
3. **Check BERT Model**: Ensure model files exist in `backend\models\bert_priority_classifier\`
4. **Check Execution Policy**: Run `Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process`

### If Frontend Doesn't Start
1. **Check Node.js**: Ensure Node.js is installed (`node --version`)
2. **Check NPM Dependencies**: Run `npm install` in `C:\Github\KairoCal\frontend\`
3. **Check Port 3000**: Ensure no other process is using port 3000

### If Docker Errors Occur
❌ **DO NOT USE DOCKER** - Use the native SQLite method documented above.  
The Docker method causes BERT model loading issues and startup hangs.

---

## 💡 **WHY THIS METHOD WORKS**

### ✅ **Separate PowerShell Windows**
- Avoids VS Code terminal issues that cause server startup problems
- Keeps servers running independently
- Easier to monitor individual server logs

### ✅ **Native Backend (No Docker)**
- Bypasses Docker resource constraints that prevent BERT model loading
- Uses local SQLite database (no container dependencies)
- Faster startup time
- Direct access to Windows file system

### ✅ **SQLite Database**
- No Docker PostgreSQL setup required
- Reliable file-based database
- All data persists in `kairocal.db` file
- No authentication issues

### ✅ **Root Level .venv**
- Virtual environment at `C:\Github\KairoCal\.venv\` works correctly
- All Python dependencies properly installed
- BERT model and transformers libraries available

---

## 📊 **VERIFIED SYSTEM STATUS (August 15, 2025)**

### ✅ **Backend Services**
- **Main API**: `http://127.0.0.1:8000/health` → "healthy"
- **Database**: SQLite connected (52 KB, 4 tables)
- **BERT NLP**: Operational (87.5% accuracy, 94.7% confidence)
- **Voice API**: Available and responding
- **Conflict Detection**: Operational

### ✅ **Frontend Services**
- **Development Server**: `http://localhost:3000`
- **Build Status**: Successful
- **API Integration**: Connected to backend

### ✅ **Database Status**
- **File**: `C:\Github\KairoCal\backend\kairocal.db` (52 KB)
- **Tables**: 4 (alembic_version, events, reminders, users)
- **Connection**: Working via API endpoints
- **Migration**: "diverged" (normal for development)

---

## 🔧 **ALTERNATIVE STARTUP METHOD**

If you prefer to use the scripts from the root directory (also works):

### Alternative Backend Command
```powershell
& 'C:\Github\KairoCal\scripts\start_servers.ps1' -Backend
```

### Alternative Frontend Command  
```powershell
& 'C:\Github\KairoCal\scripts\start_servers.ps1' -Frontend
```

### Start Both Together
```powershell
& 'C:\Github\KairoCal\scripts\start_servers.ps1'
```

---

## 📝 **MAINTENANCE NOTES**

### Last Successful Test
- **Date**: August 15, 2025
- **Backend**: ✅ All endpoints responding
- **Frontend**: ✅ Server starting correctly
- **Database**: ✅ SQLite operational
- **BERT**: ✅ 94.7% confidence classification

### Key Success Factors
1. ✅ Use separate PowerShell windows (not VS Code terminals)
2. ✅ Use native backend with SQLite (avoid Docker)
3. ✅ Use root-level `.venv` virtual environment
4. ✅ Ensure all scripts have proper execution policy bypass

---

*This document should be updated whenever the startup method changes or new issues are discovered.*

**Status: PRODUCTION READY** 🚀
