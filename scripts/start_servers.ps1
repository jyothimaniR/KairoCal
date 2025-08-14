# Start KairoCal backend and frontend in separate PowerShell windows
param(
    [switch]$Frontend,
    [switch]$Backend
)

if (-not ($Frontend -or $Backend)) {
    $Frontend = $true
    $Backend = $true
}

$root = "C:\Github\KairoCal"

if ($Backend) {
    Write-Host "Starting backend on http://127.0.0.1:8001 ..."
    $backendCmd = "& `"$root\.venv\Scripts\Activate.ps1`"; Set-Location `"$root\backend`"; python start_server.py"
    Start-Process -FilePath powershell.exe -ArgumentList @('-NoExit','-ExecutionPolicy','Bypass','-Command', $backendCmd) | Out-Null
}

if ($Frontend) {
    Write-Host "Starting frontend (Vite) on http://127.0.0.1:3000 ..."
    $frontendCmd = "Set-Location `"$root\frontend`"; npm run dev"
    Start-Process -FilePath powershell.exe -ArgumentList @('-NoExit','-ExecutionPolicy','Bypass','-Command', $frontendCmd) | Out-Null
}

Write-Host "Launch issued. Servers will open in separate PowerShell windows."
