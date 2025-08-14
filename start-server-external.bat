@echo off
title KairoCal Backend Server (SQLite)
cd /d "C:\Github\KairoCal\backend"
set DATABASE_URL=sqlite:///./kairocal.db

echo Starting KairoCal Backend Server...
echo Database: SQLite (kairocal.db)
echo Working Directory: %CD%
echo.

"..\.venv\Scripts\python.exe" start_server.py --sqlite

echo.
echo Server stopped. Press any key to close...
pause > nul
