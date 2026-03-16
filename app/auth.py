"""
API Key authentication dependency for FastAPI.
Validates the X-API-Key header against configured keys.
"""

from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader
from app.config import get_settings

# Define the API key header scheme
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


async def verify_api_key(api_key: str = Security(api_key_header)) -> str:
    """
    FastAPI dependency that validates the API key from the X-API-Key header.

    Args:
        api_key: The API key extracted from the request header.

    Returns:
        The validated API key string.

    Raises:
        HTTPException: 401 if the key is missing or invalid.
    """
    settings = get_settings()

    if api_key is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing API Key. Please provide a valid API key in the X-API-Key header.",
        )

    if api_key not in settings.api_keys_list:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key. Access denied.",
        )

    return api_key
