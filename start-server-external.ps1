# KairoCal Backend Server - External PowerShell Window Launcher
# This script will start the server in SQLite mode

Write-Host "Starting KairoCal Backend Server (SQLite Mode)" -ForegroundColor Green
Write-Host "Working Directory: C:\Github\KairoCal\backend" -ForegroundColor Yellow
Write-Host "Database: SQLite (kairocal.db)" -ForegroundColor Yellow

# Navigate to backend directory
Set-Location "C:\Github\KairoCal\backend"

# Set SQLite database URL
$env:DATABASE_URL = "sqlite:///./kairocal.db"

# Show environment
Write-Host "Environment:" -ForegroundColor Cyan
Write-Host "   DATABASE_URL: $env:DATABASE_URL" -ForegroundColor Gray
Write-Host "   Current Dir: $(Get-Location)" -ForegroundColor Gray

Write-Host ""
Write-Host "Starting server..." -ForegroundColor Green
Write-Host "=================================================="

try {
    # Start the server
    & "..\.venv\Scripts\python.exe" start_server.py --sqlite
} catch {
    Write-Host "Failed to start server: $_" -ForegroundColor Red
    Write-Host ""
    Write-Host "Press any key to continue..." -ForegroundColor Yellow
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
}

Write-Host ""
Write-Host "Server stopped. Press any key to close this window..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
