import os

from dotenv import load_dotenv


# Load variables from backend/.env
load_dotenv()


DATABASE_URL = os.getenv("DATABASE_URL")
SECRET_KEY = os.getenv("SECRET_KEY")

ALGORITHM = os.getenv(
    "ALGORITHM",
    "HS256"
)

ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv(
        "ACCESS_TOKEN_EXPIRE_MINUTES",
        "30"
    )
)


# Validate required environment variables
if not DATABASE_URL:
    raise ValueError(
        "DATABASE_URL is missing from the .env file."
    )

if not SECRET_KEY:
    raise ValueError(
        "SECRET_KEY is missing from the .env file."
    )