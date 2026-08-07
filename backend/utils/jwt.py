import hashlib
import os
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import jwt
from passlib.context import CryptContext
from backend.config import settings
from backend.logging import logger

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies plain password against stored hash with bcrypt / SHA256 fallback."""
    try:
        if hashed_password.startswith("$pbkdf2") or hashed_password.startswith("$2b$"):
            return pwd_context.verify(plain_password, hashed_password)
        # Simple SHA256 fallback for seed data or legacy compatibility
        salt, h = hashed_password.split(":") if ":" in hashed_password else ("", hashed_password)
        check_hash = hashlib.sha256((salt + plain_password).encode("utf-8")).hexdigest()
        return check_hash == h
    except Exception as e:
        logger.error(f"Password verification error: {e}")
        return False


def get_password_hash(password: str) -> str:
    """Hashes a raw password."""
    try:
        return pwd_context.hash(password)
    except Exception:
        salt = os.urandom(16).hex()
        h = hashlib.sha256((salt + password).encode("utf-8")).hexdigest()
        return f"{salt}:{h}"


def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """Generates signed JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> Optional[Dict[str, Any]]:
    """Decodes and validates JWT token."""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except jwt.PyJWTError as e:
        logger.warning(f"JWT Token validation failed: {e}")
        return None
