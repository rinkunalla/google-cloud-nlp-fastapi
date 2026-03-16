"""
FastAPI application entry point.
Sets up middleware, rate limiting, and routes.
"""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from app.config import get_settings
from app.rate_limiter import limiter
from app.routes.nlp import router as nlp_router

settings = get_settings()

# ──────────────────────────── Create App ────────────────────────────────

app = FastAPI(
    title=settings.APP_TITLE,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
)

# ──────────────────────────── Middleware ─────────────────────────────────

# Attach SlowAPI rate limiter
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    """Add basic security headers to every response."""
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    return response


# ──────────────────────────── Routes ────────────────────────────────────

app.include_router(nlp_router)


@app.get(
    "/",
    summary="Health Check",
    description="Returns the health status of the API service.",
    tags=["Health"],
)
async def health_check():
    """Health check endpoint — no authentication required."""
    return {
        "status": "healthy",
        "service": settings.APP_TITLE,
        "version": settings.APP_VERSION,
    }


@app.get(
    "/api/v1",
    summary="API Info",
    description="Returns information about available API endpoints.",
    tags=["Health"],
)
async def api_info():
    """API information endpoint — no authentication required."""
    return {
        "message": "Google Cloud Natural Language API Service",
        "version": settings.APP_VERSION,
        "endpoints": {
            "sentiment_analysis": "/api/v1/nlp/sentiment",
            "entity_analysis": "/api/v1/nlp/entities",
            "syntax_analysis": "/api/v1/nlp/syntax",
            "text_classification": "/api/v1/nlp/classify",
        },
        "documentation": "/docs",
    }
