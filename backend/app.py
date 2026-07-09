from fastapi import FastAPI

from routes.interview import router as interview_router
from routes.evaluation import router as evaluation_router
from routes.resume import router as resume_router
from routes.auth import router as auth_router
from routes.report import router as report_router 

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title = "InterviewIQ-AI",
    version = "1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174"
    ],
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