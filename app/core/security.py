"""
Security utilities for password hashing and JWT token management.
"""
from datetime import datetime, timedelta, timezone
from passlib.hash import bcrypt
from jose import jwt
from app.core.config import settings

def hash_password(plain: str) -> str:
    """
    Hashes a plain password using bcrypt.
    """
    return bcrypt.hash(plain)

def verify_password(plain: str, hashed: str) -> bool:
    """
    Verifies a plain password against a hashed password.
    """
    return bcrypt.verify(plain, hashed)

def create_access_token(
    subject: str,
    expires_minutes: int | None = None,
    extra: dict | None = None
) -> str:
    """
    Creates a JWT access token.
    """
    expire = datetime.now(tz=timezone.utc) + timedelta(
        minutes=expires_minutes or settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode = {"sub": subject, "exp": expire}
    if extra:
        to_encode.update(extra)
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

def decode_token(token: str) -> dict:
    """
    Decodes a JWT token and returns the payload.
    """
    return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
