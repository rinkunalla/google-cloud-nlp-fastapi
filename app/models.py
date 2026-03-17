from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional


class LanguageCode(str, Enum):
    """
    Language selection for Google Cloud NLP.
    - Auto_Detect (Default): Let the AI automatically identify the language.
    - (Supported): Manually select if detection fails or for specific hints.
    - (Not Supported): Features might fail as Google doesn't officially support these yet.
    """
    Auto_Detect = "Auto-detect (Recommended)"
    English_Supported = "English (Supported)"
    Spanish_Supported = "Spanish (Supported)"
    French_Supported = "French (Supported)"
    German_Supported = "German (Supported)"
    Italian_Supported = "Italian (Supported)"
    Japanese_Supported = "Japanese (Supported)"
    Korean_Supported = "Korean (Supported)"
    Portuguese_Supported = "Portuguese (Supported)"
    Dutch_Supported = "Dutch (Supported)"
    Chinese_Simplified_Supported = "Chinese_Simplified (Supported)"
    Chinese_Traditional_Supported = "Chinese_Traditional (Supported)"
    Filipino_Not_Supported = "Filipino (Not Supported)"
    Russian_Not_Supported = "Russian (Not Supported)"
    Arabic_Not_Supported = "Arabic (Not Supported)"
    Hindi_Not_Supported = "Hindi (Not Supported)"


# ──────────────────────────── Request Models ────────────────────────────


class TextRequest(BaseModel):
    """Request body for all NLP endpoints."""

    text: str = Field(
        ...,
        min_length=1,
        max_length=10000,
        description="The text content to analyze.",
        json_schema_extra={"example": "I love using Google NLP API! Masaya itong gamitin."},
    )
    language: LanguageCode = Field(
        default=LanguageCode.Auto_Detect,
        description="Select language or let the AI detect it automatically.",
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
