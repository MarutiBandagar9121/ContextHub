from pathlib import Path

import jwt

from organization_service.config.settings import settings

_PUBLIC_KEY = Path(settings.jwt_public_key_path).read_text()


def decode_token(token: str) -> dict:
    """Decodes and validates a JWT signed by auth_service, raising
    jwt.PyJWTError on failure. Verifies only — this service never signs."""
    return jwt.decode(token, _PUBLIC_KEY, algorithms=[settings.jwt_algorithm])
