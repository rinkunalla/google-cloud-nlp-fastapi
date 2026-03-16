"""
Pydantic models for request validation and response serialization.
"""

from pydantic import BaseModel, Field
from typing import Optional


# ──────────────────────────── Request Models ────────────────────────────


class TextRequest(BaseModel):
    """Request body for all NLP endpoints."""

    text: str = Field(
        ...,
        min_length=1,
        max_length=10000,
        description="The text content to analyze.",
        json_schema_extra={"example": "Google Cloud Natural Language API is amazing! I love using it for text analysis."},
    )
    language: str = Field(
        default="en",
        description="ISO 639-1 language code (e.g., 'en', 'es', 'fr').",
        json_schema_extra={"example": "en"},
    )


# ──────────────────────────── Response Models ───────────────────────────


class SentimentScore(BaseModel):
    """Sentiment score for a piece of text."""

    score: float = Field(..., description="Sentiment score between -1.0 (negative) and 1.0 (positive).")
    magnitude: float = Field(..., description="Strength of sentiment regardless of score (0.0+).")


class SentenceSentiment(BaseModel):
    """Sentiment for an individual sentence."""

    text: str
    sentiment: SentimentScore


class SentimentResponse(BaseModel):
    """Response for sentiment analysis."""

    document_sentiment: SentimentScore
    sentences: list[SentenceSentiment]
    language: str


class EntityMention(BaseModel):
    """A mention of an entity in the text."""

    text: str
    type: str


class Entity(BaseModel):
    """A named entity extracted from the text."""

    name: str
    type: str
    salience: float = Field(..., description="Importance score from 0.0 to 1.0.")
    mentions: list[EntityMention]
    metadata: dict[str, str] = Field(default_factory=dict)


class EntityResponse(BaseModel):
    """Response for entity analysis."""

    entities: list[Entity]
    language: str


class Token(BaseModel):
    """A syntax token (word) with linguistic information."""

    text: str
    part_of_speech: str
    dependency_edge: str
    lemma: str


class SyntaxResponse(BaseModel):
    """Response for syntax analysis."""

    tokens: list[Token]
    sentences: list[str]
    language: str


class Category(BaseModel):
    """A content classification category."""

    name: str = Field(..., description="Category name (e.g., '/Science/Computer Science').")
    confidence: float = Field(..., description="Confidence score from 0.0 to 1.0.")


class ClassificationResponse(BaseModel):
    """Response for text classification."""

    categories: list[Category]


class ErrorResponse(BaseModel):
    """Standard error response body."""

    detail: str = Field(..., description="Human-readable error message.")
