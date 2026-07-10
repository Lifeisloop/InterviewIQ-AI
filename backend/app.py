import os
from fastapi import FastAPI

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
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
def home():
    return {
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