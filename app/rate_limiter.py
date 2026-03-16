"""
Rate limiting configuration using SlowAPI.
Limits requests per API key to prevent abuse.
"""

from slowapi import Limiter
from slowapi.util import get_remote_address
from starlette.requests import Request
from app.config import get_settings


def get_api_key_or_ip(request: Request) -> str:
    """
    Extract the rate-limit key from the request.
    Uses the X-API-Key header if present, otherwise falls back to client IP.
    """
    api_key = request.headers.get("X-API-Key")
    if api_key:
        return api_key
    return get_remote_address(request)


# Create the limiter instance with the custom key function
limiter = Limiter(key_func=get_api_key_or_ip)


def get_rate_limit() -> str:
    """Return the configured rate limit string."""
    settings = get_settings()
    return settings.RATE_LIMIT
