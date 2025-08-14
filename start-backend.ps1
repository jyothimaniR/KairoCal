Write-Host "Starting KairoCal Backend Services..." -ForegroundColor Green
Write-Host "Starting Docker containers..." -ForegroundColor Yellow

# Navigate to project root
Set-Location "C:\Github\KairoCal"

# Start Docker services
docker compose up -d

# Wait a moment for services to initialize
Start-Sleep -Seconds 5

# Check status
Write-Host "`nChecking service status..." -ForegroundColor Yellow
docker compose ps

# Test health endpoint
Write-Host "`nTesting backend health..." -ForegroundColor Yellow
try {
    $healthResponse = Invoke-RestMethod -Uri "http://localhost:8000/health" -TimeoutSec 10
    Write-Host "Backend Health: " -NoNewline -ForegroundColor Green
    Write-Host ($healthResponse | ConvertTo-Json -Depth 2)
} catch {
    Write-Host "Backend health check failed: $_" -ForegroundColor Red
}

# Test voice endpoints specifically
Write-Host "`nTesting voice API endpoints..." -ForegroundColor Yellow
try {
    $voiceHealthResponse = Invoke-RestMethod -Uri "http://localhost:8000/api/v1/voice/health" -TimeoutSec 10
    Write-Host "Voice API Health: " -NoNewline -ForegroundColor Green
    Write-Host ($voiceHealthResponse | ConvertTo-Json -Depth 2)
} catch {
    Write-Host "Voice API health check failed: $_" -ForegroundColor Red
}

Write-Host "`nBackend services started. Keep this PowerShell window open." -ForegroundColor Green
Write-Host "Press Ctrl+C to stop services when done." -ForegroundColor Yellow

# Keep window open
Read-Host "Press Enter to stop services"
docker compose down
