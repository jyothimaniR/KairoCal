# OLD (Unix style):
cd backend && source venv/bin/activate && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# NEW (Windows style):
cd backend && source venv/Scripts/activate && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000