"""
NLP API route handlers.
All endpoints require API key authentication and are rate-limited.
"""

from fastapi import APIRouter, Depends, Request, Form
from app.auth import verify_api_key
from app.rate_limiter import limiter, get_rate_limit
from app.models import (
    LanguageCode,
    SentimentResponse,
    EntityResponse,
    SyntaxResponse,
    ClassificationResponse,
    ErrorResponse,
)
from app import nlp_service

router = APIRouter(
    prefix="/api/v1/nlp",
    tags=["Natural Language Processing"],
    dependencies=[Depends(verify_api_key)],
    responses={
        401: {"model": ErrorResponse, "description": "Invalid or missing API key"},
        429: {"description": "Rate limit exceeded"},
        500: {"model": ErrorResponse, "description": "Internal server error"},
    },
)


@router.post(
    "/sentiment",
    response_model=SentimentResponse,
    summary="Analyze Sentiment",
    description="Analyze the overall sentiment and sentence-level sentiment of the provided text. "
    "Returns a score (-1.0 to 1.0) and magnitude (0.0+) for the entire document and each sentence.",
    responses={400: {"model": ErrorResponse, "description": "Invalid request"}},
)
@limiter.limit(get_rate_limit())
async def sentiment_analysis(
    request: Request,
    text: str = Form(..., description="The text content to analyze.", json_schema_extra={"example": "I love using Google NLP API!"}),
    language: LanguageCode = Form(LanguageCode.Auto_Detect, description="Select the language of the text."),
):
    """Analyze sentiment of the provided text."""
    return await nlp_service.analyze_sentiment(text, language)


@router.post(
    "/entities",
    response_model=EntityResponse,
    summary="Extract Entities",
    description="Identify and extract named entities (people, organizations, locations, etc.) "
    "from the provided text, along with their types, salience scores, and metadata.",
    responses={400: {"model": ErrorResponse, "description": "Invalid request"}},
)
@limiter.limit(get_rate_limit())
async def entity_analysis(
    request: Request,
    text: str = Form(..., description="The text content to analyze.", json_schema_extra={"example": "Google was founded in Menlo Park."}),
    language: LanguageCode = Form(LanguageCode.Auto_Detect, description="Select the language of the text."),
):
    """Extract entities from the provided text."""
    return await nlp_service.analyze_entities(text, language)


@router.post(
    "/syntax",
    response_model=SyntaxResponse,
    summary="Analyze Syntax",
    description="Perform syntactic analysis on the provided text, returning part-of-speech tags, "
    "dependency parse trees, and lemmas for each token.",
    responses={400: {"model": ErrorResponse, "description": "Invalid request"}},
)
@limiter.limit(get_rate_limit())
async def syntax_analysis(
    request: Request,
    text: str = Form(..., description="The text content to analyze.", json_schema_extra={"example": "The quick brown fox jumps."}),
    language: LanguageCode = Form(LanguageCode.Auto_Detect, description="Select the language of the text."),
):
    """Analyze syntax of the provided text."""
    return await nlp_service.analyze_syntax(text, language)


@router.post(
    "/classify",
    response_model=ClassificationResponse,
    summary="Classify Content",
    description="Classify the provided text into content categories. "
    "**Note:** The text must contain at least 20 words for classification to work.",
    responses={400: {"model": ErrorResponse, "description": "Invalid request or text too short"}},
)
@limiter.limit(get_rate_limit())
async def text_classification(
    request: Request,
    text: str = Form(..., description="The text content to analyze.", json_schema_extra={"example": "Python is a versatile programming language used extensively in data science, machine learning, and web development."}),
    language: LanguageCode = Form(LanguageCode.Auto_Detect, description="Select the language of the text."),
):
    """Classify the content of the provided text."""
    return await nlp_service.classify_text(text, language)
