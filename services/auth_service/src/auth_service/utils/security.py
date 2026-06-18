
import hashlib

import bcrypt


def hash_password(password: str) -> str:
    """Hashes a password using a secure hashing algorithm."""
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')

def verify_hashed_password(plain_password: str, hashed_password: str)-> bool:
    """Verifies a plain password against a hashed password."""
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def hash_token(token: str) -> str:
    """Hashes an opaque token (e.g. a refresh token) for DB storage/lookup.

    Uses SHA-256 rather than bcrypt: token lookups need a deterministic hash
    so we can query by it, whereas bcrypt's per-call random salt makes that
    impossible.
    """
    return hashlib.sha256(token.encode('utf-8')).hexdigest()