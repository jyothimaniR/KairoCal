from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="KairoCal API",
    description="AI-Powered Smart Calendar System",
    version="1.0.0"
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
    return {"message": "KairoCal API is running!", "status": "healthy"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "kairocal-api"}

@app.get("/api/v1/status")
def api_status():
    return {
        "api_version": "1.0.0",
        "service": "KairoCal Backend",
        "status": "operational"
    }