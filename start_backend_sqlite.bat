@echo off
echo Starting KairoCal Backend Server in separate PowerShell window...
echo Database: SQLite mode
echo Server will run on: http://127.0.0.1:8000

start "KairoCal Backend" powershell -NoExit -Command "cd 'c:\Github\KairoCal\backend'; & '..\.venv\Scripts\python.exe' start_server.py --sqlite"

echo Backend server starting in new window...
echo Check the new PowerShell window for server status.
pause
