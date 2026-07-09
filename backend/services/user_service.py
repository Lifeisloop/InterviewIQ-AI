from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from database.models.user import User
from models.user_model import UserRegister
from utils.security import (
    hash_password,
    verify_password,
    create_access_token
)


def create_user(user_data: UserRegister, db: Session):

    # Check if the email already exists
    existing_user = (
        db.query(User)
        .filter(User.email == user_data.email)
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )

    new_user = User(
        full_name=user_data.full_name,
        email=user_data.email,
        hashed_password=hash_password(user_data.password)
    )

    db.add(new_user)

    try:
        db.commit()
        db.refresh(new_user)

    except Exception:
        db.rollback()
        raise

    return new_user


def authenticate_user(
    email: str,
    password: str,
    db: Session
):

    # Find user by email
    user = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    # Check user exists
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Verify password
    if not verify_password(
        password,
        user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Create JWT token
    access_token = create_access_token(
        data={
            "sub": str(user.id)
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }