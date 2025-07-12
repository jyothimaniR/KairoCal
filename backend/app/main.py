# backend/app/main.py
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.core.database import get_db, engine
from app.config import get_settings

settings = get_settings()

app = FastAPI(
    title="KairoCal API",
    description="AI-Powered Smart Calendar System",
    version="1.0.0",
    debug=settings.debug
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {
        "message": "KairoCal API is running!",
        "status": "healthy",
        "version": "1.0.0"
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "kairocal-api",
        "database": "connected"
    }

@app.get("/api/v1/status")
def api_status():
    return {
        "api_version": "1.0.0",
        "service": "KairoCal Backend",
        "status": "operational",
        "features": [
            "User Management",
            "Event Scheduling", 
            "Smart Reminders",
            "NLP Processing (Coming Soon)"
        ]
    }

@app.get("/api/v1/database/status")
def database_status(db: Session = Depends(get_db)):
    """Check database connectivity and table status"""
    try:
        # Test database connection
        from sqlalchemy import text
        result = db.execute(text("SELECT 1"))
        result.fetchone()
        
        # Check if tables exist
        from sqlalchemy import inspect
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        return {
            "database_status": "connected",
            "tables_created": len(tables),
            "tables": tables,
            "models_registered": ["users", "events", "reminders"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

# Development endpoint to create tables manually
@app.post("/api/v1/database/create-tables")
def create_tables_endpoint():
    """Create database tables (development only)"""
    try:
        from app.core.database import Base
        Base.metadata.create_all(bind=engine)
        
        from sqlalchemy import inspect
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        return {
            "message": "Tables created successfully",
            "tables_created": tables
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Table creation failed: {str(e)}")