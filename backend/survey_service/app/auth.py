# app/auth.py
# Simple bearer token check using SECRET_TOKEN

from flask import request
from app.config.config import Config

class AuthError(Exception):
    """Raised when auth fails."""

def require_token_or_raise():
    """
    Expect header: Authorization: Bearer <SECRET_TOKEN>
    Raises AuthError if missing/invalid.
    """
    header = request.headers.get("Authorization", "")
    if not header.startswith("Bearer "):
        raise AuthError("Missing or invalid Authorization header")
    token = header.split(" ", 1)[1].strip()
    if token != Config.SECRET_TOKEN:
        raise AuthError("Invalid token")
