# InterviewIQ AI

An AI-powered full-stack interview preparation platform that analyzes resumes, generates personalized interview questions, evaluates candidate answers, and produces detailed performance reports.

## Overview

InterviewIQ AI helps candidates practice job-specific interviews through an intelligent and personalized workflow.

The platform extracts information from an uploaded resume, identifies candidate skills, considers the target job description, generates interview questions across multiple difficulty levels, evaluates answers using a local Large Language Model, and creates a final interview performance report.

## Features

- User registration and login
- JWT-based authentication
- Protected frontend routes
- PDF resume upload
- Resume information extraction
- Candidate name, email, phone, and skill extraction
- Resume-based interview personalization
- Job-description-aware question generation
- AI-generated interview questions
- Multiple question categories and difficulty levels
- Candidate answer evaluation
- Score generation out of 10
- Strength and weakness analysis
- Ideal answer generation
- Final interview performance report
- Interactive React frontend
- REST API backend
- SQLite / MySQL database integration
- Cloud LLM integration using Groq Cloud API

## Interview Categories

The system can generate questions across categories such as:

- Easy
- Medium
- Hard
- Coding
- HR

Questions are personalized using candidate skills extracted from the uploaded resume and the target job description.

## Tech Stack

### Frontend

- React
- Vite
- JavaScript
- CSS
- Axios
- React Router

### Backend

- Python
- FastAPI
- Uvicorn
- SQLAlchemy
- Pydantic
- PyMySQL
- python-jose
- bcrypt
- PyMuPDF (for PDF Resume parsing)

### Database

- SQLite (default)
- MySQL (supported)

### AI and NLP

- Groq Cloud API (Llama 3.3 70B - Free cloud LLM)
- Prompt Engineering
- AI-based answer evaluation
- Resume information extraction

### Authentication

- JWT (JSON Web Tokens)
- bcrypt password hashing

### Development Tools

- Git
- GitHub
- VS Code
- Swagger UI
- MySQL Workbench

## System Workflow

1. User creates an account or logs in.
2. Backend generates a JWT access token.
3. User uploads a PDF resume.
4. The system extracts candidate information and technical skills.
5. User provides a target job description.
6. The platform generates personalized interview questions.
7. Candidate answers interview questions.
8. AI evaluates each answer.
9. The system calculates scores.
10. Strengths and weaknesses are identified.
11. Ideal answers are generated.
12. A final interview report is displayed.

## Project Architecture

```text
InterviewIQ-AI/
├── backend/
│   ├── ai/
│   │   ├── evaluation_prompt.py
│   │   ├── llm.py
│   │   └── prompt_builder.py
│   │
│   ├── database/
│   │   ├── models/
│   │   ├── base.py
│   │   └── connection.py
│   │
│   ├── models/
│   │   ├── ats_model.py
│   │   ├── evaluation.py
│   │   ├── interview_model.py
│   │   ├── report_model.py
│   │   ├── resume_model.py
│   │   └── user_model.py
│   │
│   ├── routes/
│   │   ├── auth.py
│   │   ├── evaluation.py
│   │   ├── interview.py
│   │   ├── report.py
│   │   └── resume.py
│   │
│   ├── services/
│   │   ├── evaluation_service.py
│   │   ├── information_extractor.py
│   │   ├── interview_service.py
│   │   ├── report_service.py
│   │   ├── resume_parser.py
│   │   ├── resume_service.py
│   │   └── user_service.py
│   │
│   ├── utils/
│   │   ├── dependencies.py
│   │   └── security.py
│   │
│   ├── app.py
│   ├── config.py
│   ├── create_tables.py
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── api/
│   │   │   └── api.js
│   │   ├── components/
│   │   │   └── ProtectedRoute.jsx
│   │   ├── pages/
│   │   │   ├── Dashboard.jsx
│   │   │   ├── Interview.jsx
│   │   │   ├── Login.jsx
│   │   │   └── Register.jsx
│   │   ├── styles/
│   │   │   ├── auth.css
│   │   │   ├── dashboard.css
│   │   │   ├── global.css
│   │   │   └── interview.css
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   ├── vite.config.js
│   └── .env.example
│
├── .gitignore
└── README.md
```

## API Endpoints

### Authentication

| Method | Endpoint | Description |
| --- | --- | --- |
| POST | `/auth/register` | Register a new user |
| POST | `/auth/login` | Authenticate user and return JWT |
| GET | `/auth/me` | Get authenticated user profile |

### Resume

| Method | Endpoint | Description |
| --- | --- | --- |
| POST | `/resume/upload-resume` | Upload and analyze a PDF resume |

### Interview

| Method | Endpoint | Description |
| --- | --- | --- |
| POST | `/interview/generate` | Generate AI interview questions |
| POST | `/interview/start` | Start an interview session |

### Evaluation

| Method | Endpoint | Description |
| --- | --- | --- |
| POST | `/evaluation/evaluate` | Evaluate a candidate answer |

### Report

| Method | Endpoint | Description |
| --- | --- | --- |
| POST | `/report/final` | Generate final interview report |

## Local Setup

### Prerequisites

Install the following:

- Python 3.11+
- Node.js
- Git

## Backend Setup

Move into the backend directory:

```bash
cd backend
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file using `.env.example` as a reference:

```env
DATABASE_URL=sqlite:///database.db
LLM_PROVIDER=groq
GROQ_API_KEY=your_groq_api_key_here
SECRET_KEY=your_secure_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Start the backend:

```bash
python -m uvicorn app:app --reload
```

Backend API:

```text
http://127.0.0.1:8000
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

## Frontend Setup

Open another terminal and move into the frontend directory:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Create a frontend `.env` file:

```env
VITE_API_BASE_URL=http://127.0.0.1:8000
```

Start the frontend:

```bash
npm run dev
```

Frontend application:

```text
http://localhost:5173
```

The actual Vite port may differ if port `5173` is already in use.

## Environment Variables

Real environment files are intentionally excluded from Git.

Never commit:

```text
backend/.env
frontend/.env
```

Use these template files instead:

```text
backend/.env.example
frontend/.env.example
```

## Screenshots

### Login Page

![Login Page](screenshots/login.png)

### Registration Page

![Registration Page](screenshots/register.png)

### Resume Upload Dashboard

![Resume Upload Dashboard](screenshots/dashboard.png)

### AI Interview Page

![AI Interview Page](screenshots/interview.png)

## Cloud Deployment

The application is deployed and running live in the cloud:

* **Frontend (Vercel)**: [https://interview-iq-ai-roan.vercel.app/](https://interview-iq-ai-roan.vercel.app/)
* **Backend (Render)**: [https://interviewiq-ai-r4p3.onrender.com/](https://interviewiq-ai-r4p3.onrender.com/)

### Production Configuration (Render Environment Variables)
* `LLM_PROVIDER`: Set to `groq` (to use the free Groq Cloud API).
* `GROQ_API_KEY`: Your Groq Cloud API secret key.
* `DATABASE_URL`: Set to `sqlite:///database.db` (temporary file-based SQLite database) or your persistent cloud MySQL URL.

## Future Improvements

- Speech-to-text interview answers
- Voice-based AI interviewer
- Webcam-based interview simulation
- Answer timer
- Interview history dashboard
- PDF report export
- ATS resume scoring
- Advanced analytics
- Docker support
- Automated testing
- Role-specific interview templates

## Security

- Passwords are hashed using bcrypt.
- Authentication uses JWT access tokens.
- Protected APIs validate bearer tokens.
- Sensitive configuration is stored in environment variables.
- Real `.env` files are excluded from Git.

## Author

**Kush Gupta**

GitHub: `Lifeisloop`

## License

This project is intended for educational and portfolio purposes.
