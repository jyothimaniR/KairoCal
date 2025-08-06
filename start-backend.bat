@echo off
echo 🚀 Starting KairoCal Backend Server...
echo.
echo 📍 Activating virtual environment...
cd /d "C:\Github\KairoCal"
call .venv\Scripts\activate.bat

echo 📍 Starting server on http://localhost:8001...
cd backend
python start_server.py

pause
