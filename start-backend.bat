@echo off
echo 🚀 Starting KairoCal Backend Server...
echo.
echo 📍 Activating virtual environment...
cd /d "C:\Github\KairoCal"
call .venv\Scripts\activate.bat

set API_PORT=8000
echo 📍 Starting server on http://localhost:%API_PORT%...
cd backend
python start_server.py

pause
