import secrets

def generate_otp(length: int = 6) -> str:
    """Generates a secure random OTP of the specified length."""
    return ''.join(secrets.choice('0123456789') for _ in range(length))