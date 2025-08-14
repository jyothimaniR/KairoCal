@echo off
cd /d "C:\Github\KairoCal\backend"
REM Activate the root-level .venv (one level up from backend)
call ..\.venv\Scripts\activate.bat
python run_server.py
pause
