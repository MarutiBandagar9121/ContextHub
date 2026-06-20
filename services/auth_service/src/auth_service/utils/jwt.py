import secrets
from datetime import datetime, timedelta, timezone
from pathlib import Path

import jwt

from auth_service.config.settings import settings

_PRIVATE_KEY = Path(settings.jwt_private_key_path).read_text()
_PUBLIC_KEY = Path(settings.jwt_public_key_path).read_text()


def _create_token(payload: dict, expires_delta: timedelta) -> str:
    now = datetime.now(timezone.utc)
    full_payload = {
        **payload,
        "iat": now,
        "exp": now + expires_delta,
    }
    return jwt.encode(full_payload, _PRIVATE_KEY, algorithm=settings.jwt_algorithm)


def create_access_token(user_id: int, email: str) -> str:
    """Creates a short-lived access token carrying the user's id and email."""
    payload = {"sub": str(user_id), "email": email, "type": "access"}
    return _create_token(payload, timedelta(minutes=settings.access_token_expire_minutes))


def create_refresh_token(user_id: int) -> str:
    """Creates a long-lived refresh token. Includes a random jti so repeated
    issuance for the same user never collides on the hashed token_hash column."""
    payload = {"sub": str(user_id), "type": "refresh", "jti": secrets.token_urlsafe(16)}
    return _create_token(payload, timedelta(days=settings.refresh_token_expire_days))


def decode_token(token: str) -> dict:
    """Decodes and validates a JWT, raising jwt.PyJWTError on failure."""
    return jwt.decode(token, _PUBLIC_KEY, algorithms=[settings.jwt_algorithm])
