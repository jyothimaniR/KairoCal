# KairoCal Frontend Server - External PowerShell Window Launcher
Write-Host "Starting KairoCal Frontend Server" -ForegroundColor Green
Write-Host "Working Directory: C:\Github\KairoCal\frontend" -ForegroundColor Yellow
Write-Host "Server will run on: http://localhost:3000" -ForegroundColor Yellow

# Navigate to frontend directory
Set-Location "C:\Github\KairoCal\frontend"

# Show current directory
Write-Host ""
Write-Host "Environment:" -ForegroundColor Cyan
Write-Host "   Current Dir: $(Get-Location)" -ForegroundColor Gray
Write-Host "   Node Version: $(node --version 2>$null)" -ForegroundColor Gray

Write-Host ""
Write-Host "Starting frontend server..." -ForegroundColor Green
Write-Host "=================================================="

try {
    # Start the frontend server (Vite uses 'dev' not 'start')
    npm run dev
} catch {
    Write-Host "Failed to start frontend server: $_" -ForegroundColor Red
    Write-Host ""
    Write-Host "Press any key to continue..." -ForegroundColor Yellow
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
}

Write-Host ""
Write-Host "Frontend server stopped. Press any key to close this window..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
