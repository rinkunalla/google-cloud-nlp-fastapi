"""
Google Cloud Natural Language API service wrapper using v1.
Encapsulates all NLP operations with proper error handling.
"""

import os
from fastapi import HTTPException, status
from google.cloud import language_v1
from google.api_core.exceptions import GoogleAPICallError, InvalidArgument
from app.config import get_settings


# Map pretty names from UI to ISO-639-1 codes for Google API
ISO_LANGUAGE_MAPPING = {
    "Auto-detect (Recommended)": None,  # Special case for auto-detection
    "English (Supported)": "en",
    "Spanish (Supported)": "es",
    "French (Supported)": "fr",
    "German (Supported)": "de",
    "Italian (Supported)": "it",
    "Japanese (Supported)": "ja",
    "Korean (Supported)": "ko",
    "Portuguese (Supported)": "pt",
    "Dutch (Supported)": "nl",
    "Chinese_Simplified (Supported)": "zh",
    "Chinese_Traditional (Supported)": "zh-Hant",
    "Filipino (Not Supported)": "fil",
    "Russian (Not Supported)": "ru",
    "Arabic (Not Supported)": "ar",
    "Hindi (Not Supported)": "hi",
}


def _get_client() -> language_v1.LanguageServiceClient:
    """
    Create and return a Google Cloud Language client.
    Supports two authentication methods:
      1. API Key (simple string)
      2. Service Account JSON — fallback, set GOOGLE_APPLICATION_CREDENTIALS
    """
    settings = get_settings()

    # Method 1: API Key authentication
    if settings.GOOGLE_CLOUD_API_KEY:
        return language_v1.LanguageServiceClient(
            client_options={"api_key": settings.GOOGLE_CLOUD_API_KEY}
        )

    # Method 2: Service Account JSON file
    if settings.GOOGLE_APPLICATION_CREDENTIALS:
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = settings.GOOGLE_APPLICATION_CREDENTIALS

    return language_v1.LanguageServiceClient()


def _build_document(text: str, language: str = "Auto-detect (Recommended)") -> language_v1.Document:
    """Build a Document object for the API request."""
    # Convert pretty name to ISO code if possible
    iso_code = ISO_LANGUAGE_MAPPING.get(language, language)

    doc = language_v1.Document(
        content=text,
        type_=language_v1.Document.Type.PLAIN_TEXT,
    )

    # Only set language if it's not Auto-detect
    if iso_code:
        doc.language = iso_code

    return doc


async def analyze_sentiment(text: str, language: str = "en") -> dict:
    """Analyze the sentiment of the given text."""
    try:
        client = _get_client()
        document = _build_document(text, language)
        response = client.analyze_sentiment(
            request={"document": document, "encoding_type": language_v1.EncodingType.UTF8}
        )

        sentences = []
        for sentence in response.sentences:
            sentences.append({
                "text": sentence.text.content,
                "sentiment": {
                    "score": round(sentence.sentiment.score, 4),
                    "magnitude": round(sentence.sentiment.magnitude, 4),
                },
            })

        return {
            "document_sentiment": {
                "score": round(response.document_sentiment.score, 4),
                "magnitude": round(response.document_sentiment.magnitude, 4),
            },
            "sentences": sentences,
            "language": response.language,
        }

    except InvalidArgument as e:
        msg = str(e)
        if "language" in msg.lower() and "not supported" in msg.lower():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="This specific feature (e.g. Sentiment/Entities) is not yet supported by Google for this language. Please try English or Spanish."
            )
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid request: {msg}")
    except GoogleAPICallError as e:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=f"Google Cloud API error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An unexpected error occurred: {str(e)}")


async def analyze_entities(text: str, language: str = "en") -> dict:
    """Extract named entities from the text."""
    try:
        client = _get_client()
        document = _build_document(text, language)
        response = client.analyze_entities(
            request={"document": document, "encoding_type": language_v1.EncodingType.UTF8}
        )

        entities = []
        for entity in response.entities:
            mentions = []
            for mention in entity.mentions:
                mentions.append({
                    "text": mention.text.content,
                    "type": language_v1.EntityMention.Type(mention.type_).name,
                })

            entities.append({
                "name": entity.name,
                "type": language_v1.Entity.Type(entity.type_).name,
                "salience": round(entity.salience, 4),
                "mentions": mentions,
                "metadata": dict(entity.metadata),
            })

        return {
            "entities": entities,
            "language": response.language,
        }

    except InvalidArgument as e:
        msg = str(e)
        if "language" in msg.lower() and "not supported" in msg.lower():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="This specific feature (e.g. Sentiment/Entities) is not yet supported by Google for this language. Please try English or Spanish."
            )
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid request: {msg}")
    except GoogleAPICallError as e:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=f"Google Cloud API error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An unexpected error occurred: {str(e)}")


async def analyze_syntax(text: str, language: str = "en") -> dict:
    """Analyze the syntax (POS tags, dependency tree, etc.)."""
    try:
        client = _get_client()
        document = _build_document(text, language)
        response = client.analyze_syntax(
            request={"document": document, "encoding_type": language_v1.EncodingType.UTF8}
        )

        tokens = []
        for token in response.tokens:
            tokens.append({
                "text": token.text.content,
                "part_of_speech": language_v1.PartOfSpeech.Tag(token.part_of_speech.tag).name,
                "dependency_edge": language_v1.DependencyEdge.Label(token.dependency_edge.label).name,
                "lemma": token.lemma,
            })

        sentences = [s.text.content for s in response.sentences]

        return {
            "tokens": tokens,
            "sentences": sentences,
            "language": response.language,
        }

    except InvalidArgument as e:
        msg = str(e)
        if "language" in msg.lower() and "not supported" in msg.lower():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="This specific feature (e.g. Sentiment/Entities) is not yet supported by Google for this language. Please try English or Spanish."
            )
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid request: {msg}")
    except GoogleAPICallError as e:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=f"Google Cloud API error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An unexpected error occurred: {str(e)}")


async def classify_text(text: str, language: str = "en") -> dict:
    """Classify the content of the given text into categories."""
    try:
        word_count = len(text.split())
        if word_count < 20:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Text must contain at least 20 words. Current: {word_count}.")

        client = _get_client()
        document = _build_document(text, language)
        response = client.classify_text(request={"document": document})

        categories = []
        for category in response.categories:
            categories.append({
                "name": category.name,
                "confidence": round(category.confidence, 4),
            })

        return {
            "categories": categories,
            "detected_language": response.language if hasattr(response, "language") else "en"
        }

    except HTTPException:
        raise
    except InvalidArgument as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid request: {str(e)}")
    except GoogleAPICallError as e:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=f"Google Cloud API error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An unexpected error occurred: {str(e)}")
