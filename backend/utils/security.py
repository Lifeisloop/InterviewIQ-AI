import bcrypt

from datetime import datetime, timedelta, timezone
from typing import Optional

from jose import JWTError, jwt

from config import (
    SECRET_KEY,
    ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)


def hash_password(password: str) -> str:
    """
    Hash a plain-text password using bcrypt.
    """

    if not password:
        raise ValueError(
            "Password cannot be empty."
        )

    password_bytes = password.encode("utf-8")

    hashed_bytes = bcrypt.hashpw(
        password_bytes,
        bcrypt.gensalt()
    )

    return hashed_bytes.decode("utf-8")


def verify_password(
    plain_password: str,
    hashed_password: str
) -> bool:
    """
    Verify a plain-text password against
    a stored bcrypt password hash.
    """

    if not plain_password or not hashed_password:
        return False

    try:
        return bcrypt.checkpw(
            plain_password.encode("utf-8"),
            hashed_password.encode("utf-8")
        )

    except (
        ValueError,
        TypeError
    ):
        return False


def create_access_token(
    data: dict
) -> str:
    """
    Create a signed JWT access token.
    """

    payload = data.copy()

    expire = (
        datetime.now(timezone.utc)
        + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    )

    payload.update({
        "exp": expire
    })

    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token


def decode_access_token(
    token: str
) -> Optional[dict]:
    """
    Decode and validate a JWT access token.

    Returns the decoded payload when valid.
    Returns None when invalid or expired.
    """

    if not token:
        return None

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return payload

    except JWTError:
        return None