from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database.connection import get_db
from models.user_model import (
    UserRegister,
    UserResponse,
    UserLogin,
    TokenResponse
)
from services.user_service import (create_user, authenticate_user)

from database.models.user import User
from utils.dependencies import get_current_user


router = APIRouter()


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def register_user(
    user_data: UserRegister,
    db: Session = Depends(get_db)
):
    return create_user(
        user_data=user_data,
        db=db
    )

@router.post(
    "/login",
    response_model=TokenResponse
)
def login_user(
    login_data: UserLogin,
    db: Session = Depends(get_db)
):

    return authenticate_user(
        email=login_data.email,
        password=login_data.password,
        db=db
    )

@router.get(
    "/me",
    response_model=UserResponse
)
def get_my_profile(
    current_user: User = Depends(get_current_user)
):
    return current_user