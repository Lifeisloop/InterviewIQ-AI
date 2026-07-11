import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from routes.interview import router as interview_router
from routes.evaluation import router as evaluation_router
from routes.resume import router as resume_router
from routes.auth import router as auth_router
from routes.report import router as report_router 

from fastapi.middleware.cors import CORSMiddleware
from database.connection import engine
from database.base import Base
# Import models to register them on Base metadata for auto-creation
from database.models.user import User
from database.models.resume import Resume
from database.models.interview import Interview

# Auto-initialize database tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title = "InterviewIQ-AI",
    version = "1.0"
)

# Load allowed origins from environment variable
allowed_origins_env = os.getenv("ALLOWED_ORIGINS")
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:5174",
    "http://127.0.0.1:5174"
]
if allowed_origins_env:
    for origin in allowed_origins_env.split(","):
        cleaned = origin.strip()
        if cleaned:
            origins.append(cleaned)
            # Add version without trailing slash, and version with trailing slash
            if cleaned.endswith("/"):
                origins.append(cleaned[:-1])
            else:
                origins.append(cleaned + "/")

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex="https://.*|http://localhost:.*|http://127.0.0.1:.*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "message": "InterviewIQ AI Backend Running Successfully.."
    }

#Interview Router
app.include_router(
    interview_router,
    prefix = "/interview",
    tags = ["Interview"]
)

#Evaluation Router
app.include_router(
    evaluation_router,
    prefix = "/evaluation",
    tags = ["Evaluation"]
)

#Resume Router
app.include_router(
    resume_router,
    prefix = "/resume",
    tags = ["Resume"]
)

#Authentication Router
app.include_router(
    auth_router,
    prefix = "/auth",
    tags = ["Authentication"]
)

#Report Router
app.include_router(
    report_router,
    prefix="/report",
    tags=["Report"]
)

# Serve static React frontend files in production
DIST_DIR = os.path.join(os.path.dirname(__file__), "../frontend/dist")

if os.path.exists(DIST_DIR):
    # Mount the Vite assets folder
    assets_dir = os.path.join(DIST_DIR, "assets")
    if os.path.exists(assets_dir):
        app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")

    # Catch-all route to serve the React SPA
    @app.get("/{catchall:path}")
    def serve_spa(catchall: str):
        # Serve exact file if it exists in the build output (like favicon.svg, manifest.json, etc.)
        file_path = os.path.join(DIST_DIR, catchall)
        if catchall and os.path.isfile(file_path):
            return FileResponse(file_path)
        
        # Default fallback to serve index.html for React Router client routes
        index_path = os.path.join(DIST_DIR, "index.html")
        if os.path.exists(index_path):
            return FileResponse(index_path)
        
        return {"error": "Frontend index.html not found."}
else:
    # Fallback endpoint if frontend isn't built yet
    @app.get("/{catchall:path}")
    def serve_fallback(catchall: str):
        return {
            "error": "Frontend build files not found. Please run 'npm run build' inside the frontend folder."
        }