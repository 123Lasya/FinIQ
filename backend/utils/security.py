import hashlib
import os
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import jwt
from passlib.context import CryptContext
from backend.config import settings
from backend.utils.logger import get_logger

logger = get_logger("finpilot.security")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hashes plain text password."""
    try:
        return pwd_context.hash(password)
    except Exception:
        salt = os.urandom(16).hex()
        h = hashlib.sha256((salt + password).encode("utf-8")).hexdigest()
        return f"{salt}:{h}"


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies plain password against stored hash with fallback support."""
    try:
        if hashed_password.startswith("$2b$") or hashed_password.startswith("$pbkdf2"):
            return pwd_context.verify(plain_password, hashed_password)
        salt, h = hashed_password.split(":") if ":" in hashed_password else ("", hashed_password)
        check = hashlib.sha256((salt + plain_password).encode("utf-8")).hexdigest()
        return check == h
    except Exception as e:
        logger.error(f"Password verification error: {e}")
        return False


def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """Encodes JWT access token."""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_access_token(token: str) -> Optional[Dict[str, Any]]:
    """Decodes and validates JWT token."""
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except jwt.PyJWTError as e:
        logger.warning(f"Failed JWT token decode: {e}")
        return None
