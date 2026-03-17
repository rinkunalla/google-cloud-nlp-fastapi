# 🌐 Google Cloud Natural Language API Service

A production-ready **FastAPI** application that integrates with the **Google Cloud Natural Language API** to provide text analysis capabilities — including sentiment analysis, entity extraction, syntax analysis, and content classification — behind **authenticated** and **rate-limited** endpoints.

---

## ✨ Features

- **Sentiment Analysis** — Determine the overall sentiment (positive/negative) and emotional magnitude of text.
- **Entity Extraction** — Identify people, organizations, locations, and events with metadata.
- **Syntax Analysis** — Get part-of-speech tags and dependency parse trees.
- **Content Classification** — Categorize text into content categories (requires 20+ words).
- **Smart Auto-detection** — Zero configuration required; the API automatically identifies the language of your text.
- **Form-Based Swagger UI** — Easy testing via `/docs` with dropdowns and individual input boxes.
- **API Key Authentication** — Secure endpoints via `X-API-Key` header validation.
- **Rate Limiting** — Prevent abuse with configurable per-key request limits (default: 10 requests/minute).
- **Comprehensive Error Handling** — Meaningful error messages for language support and invalid requests.

---

## 📋 Prerequisites

| Requirement | Details |
|---|---|
| **Python** | 3.10 or higher |
| **Google Cloud Account** | With billing enabled (Free Tier available) |
| **Google Cloud Project** | Natural Language API enabled |
| **Service Account Key** | Primary authentication method (JSON) |
| **Google Cloud API Key** | Alternative authentication method (simpler) |

---

## 🌍 Supported Languages

The Google Cloud Natural Language API support varies by feature.

| Feature | Supported Languages (ISO-639-1) |
|---|---|
| **Sentiment Analysis** | `en, es, fr, de, it, ja, ko, pt, zh, zh-Hant` |
| **Entity Analysis** | `en, es, fr, de, it, ja, ko, pt, zh, zh-Hant` |
| **Syntax Analysis** | `en, es, fr, de, it, ja, ko, pt, zh, zh-Hant` |
| **Content Classification** | Primarily `en` (v2 supports more, but v1 is optimized for English) |

> **Note on Filipino (Tagalog):** Currently, the Google Cloud Natural Language API does **not** support Sentiment, Entity, or Syntax analysis for Filipino (`fil`). If you try to analyze Filipino text with these features, the API will return a `400 Bad Request` error. Currently, Filipino is only supported for **Translation API** or **Cloud Speech-to-Text**, but not for the Natural Language analysis suite.

### 💡 Pro-Tips for Language Detection

To get the most accurate results, keep these two rules in mind:

1.  **Use Native Script (Mandatory for Accuracy)**: 
    *   If you are analyzing Japanese, Chinese, or Arabic, you **MUST** use their native characters (e.g., `こんにちは`). 
    *   Using English letters for these languages (e.g., *Konnichiwa*) is called **Romanization**, and it is **not supported** by the Natural Language AI.
2.  **How "Auto-detect" Works**:
    *   By default, the API is set to **Auto-detect**. It is very smart at identifying the language based on the alphabet/script you use.
    *   If you use English letters (`A-Z`), the AI will almost always assume you are speaking **English**, even if the words are Japanese (like "konichiwaa").
    *   **The Fix:** If you want to analyze "Romanized" text, you must **manually select** the language from the dropdown menu to "force" the AI to use that specific model.


### Google Cloud Setup

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project (or select an existing one).
3. Enable the **Cloud Natural Language API**:
   - Navigate to **APIs & Services → Library**.
   - Search for "Cloud Natural Language API" and click **Enable**.
4. Create a **Service Account**:
   - Navigate to **IAM & Admin → Service Accounts**.
   - Click **Create Service Account**, give it a name, and grant the role **Cloud Natural Language API User**.
   - Click **Keys → Add Key → Create New Key → JSON**.
   - Download the JSON key file and save it securely in your project directory.

---

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/rinkunalla/google-cloud-nlp-fastapi.git
cd google-cloud-nlp-fastapi
```

### 2. Create a Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

```bash
# Copy the example environment file
cp .env.example .env
```

Edit `.env` with your settings (see Configuration Guide below).

### 5. Run the Application

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`. Visit `http://localhost:8000/docs` for the interactive Swagger UI.

---

## 🏁 Quick Start Guide (Step-by-Step)

Follow these steps **after installation** to get everything running:

### Step 1: Set Up Service Account JSON Key

1. Go to the [Google Cloud Console](https://console.cloud.google.com/iam-admin/serviceaccounts).
2. Create a **Service Account** and grant it the **Cloud Natural Language API User** role.
3. Generate and download a **JSON Key** for that account.
4. Place the `.json` file in the project root folder.

### Step 2: Configure Your `.env` File

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```
2. Open `.env` and update your keys:
   ```env
    # Option 1: Service Account JSON (Recommended)
    GOOGLE_APPLICATION_CREDENTIALS=./cnl-api-490312-7e74fbb63952.json

    # Option 2: YOUR GOOGLE CLOUD API KEY (Alternative)
    # GOOGLE_CLOUD_API_KEY=your-api-key-here

   # YOUR CUSTOM APP KEYS (any string)
   API_KEYS="Input Your Custom App Keys Here. use comma as separator to add more keys"

   # RATE LIMIT
   RATE_LIMIT=10/minute
   ```

> **Tip:** Generate strong API keys using Python:
> ```bash
> python -c "import secrets; print(secrets.token_urlsafe(32))"
> ```

### Step 3: Run and Verify

```bash
python -m uvicorn app.main:app --reload
```

Once the server is running, visit `http://localhost:8000/docs` to test the endpoints!

Then open your browser to `http://localhost:8000/docs`. This is the **recommended** way to test. We have specially designed the Swagger UI to use **Form-based inputs** (instead of raw JSON) and a **Smart Dropdown** for language selection.

---

## ⚙️ Configuration Guide

### Environment Variables

Create a `.env` file in the project root with the following variables:

| Variable | Description | Example |
|---|---|---|
| `GOOGLE_APPLICATION_CREDENTIALS` | Path to your Google Cloud service account JSON key file | `./cnl-api-490312-7e74fbb63952.json` |
| `API_KEYS` | Comma-separated list of valid keys for your users | `key-1,key-2` |
| `RATE_LIMIT` | Maximum requests per time window per API key | `10/minute` |

### Example `.env` File

```env
GOOGLE_APPLICATION_CREDENTIALS=./cnl-api-490312-7e74fbb63952.json
API_KEYS=test-api-key-1,test-api-key-2
RATE_LIMIT=10/minute
```

### Setting Up Google Cloud Credentials

1. Place the downloaded JSON key file in the project root directory.
2. Set `GOOGLE_APPLICATION_CREDENTIALS` in `.env` to the path of the key file.
3. Alternatively, set the environment variable directly:
   ```bash
   # Windows
   set GOOGLE_APPLICATION_CREDENTIALS=C:\path\to\your\service-account.json

   # macOS/Linux
   export GOOGLE_APPLICATION_CREDENTIALS=/path/to/your/service-account.json
   ```

---

## 📡 API Endpoints Documentation

### Base URL

```
http://localhost:8000
```

### Authentication

All `/api/v1/nlp/*` endpoints require an API key passed via the `X-API-Key` header.

### Endpoints

#### `GET /` — Health Check

No authentication required.

```bash
curl http://localhost:8000/
```

**Response (200):**

```json
{
  "status": "healthy",
  "service": "Google Cloud Natural Language API Service",
  "version": "1.0.0"
}
```

---

#### `POST /api/v1/nlp/sentiment` — Analyze Sentiment

Analyzes the sentiment of the provided text, returning document-level and sentence-level scores.

**Request:**

```bash
curl -X POST http://localhost:8000/api/v1/nlp/sentiment \
  -H "X-API-Key: my-secret-key-1" \
  -F "text=I absolutely love this product! It works perfectly." \
  -F "language=Auto-detect (Recommended)"
```

> **Note:** The `language` field is optional. If omitted, it defaults to Auto-detect.
```

**Response (200):**

```json
{
  "document_sentiment": {
    "score": 0.4,
    "magnitude": 1.6
  },
  "sentences": [
    {
      "text": "I absolutely love this product!",
      "sentiment": { "score": 0.9, "magnitude": 0.9 }
    },
    {
      "text": "It works perfectly.",
      "sentiment": { "score": 0.8, "magnitude": 0.8 }
    },
    {
      "text": "However, the packaging was damaged.",
      "sentiment": { "score": -0.6, "magnitude": 0.6 }
    }
  ],
  "language": "en"
}
```

---

#### `POST /api/v1/nlp/entities` — Extract Entities

Identifies named entities in the text with their types, salience scores, and metadata.

**Request:**

```bash
curl -X POST http://localhost:8000/api/v1/nlp/entities \
  -H "X-API-Key: my-secret-key-1" \
  -F "text=Google was founded in Menlo Park, California."
```
```

**Response (200):**

```json
{
  "entities": [
    {
      "name": "Google",
      "type": "ORGANIZATION",
      "salience": 0.52,
      "mentions": [{ "text": "Google", "type": "PROPER" }],
      "metadata": { "wikipedia_url": "https://en.wikipedia.org/wiki/Google" }
    },
    {
      "name": "Larry Page",
      "type": "PERSON",
      "salience": 0.18,
      "mentions": [{ "text": "Larry Page", "type": "PROPER" }],
      "metadata": {}
    }
  ],
  "language": "en"
}
```

---

#### `POST /api/v1/nlp/syntax` — Analyze Syntax

Returns part-of-speech tags, dependency parse information, and lemmas for each word.

**Request:**

```bash
curl -X POST http://localhost:8000/api/v1/nlp/syntax \
  -H "X-API-Key: my-secret-key-1" \
  -F "text=The quick brown fox jumps over the lazy dog."
```
```

**Response (200):**

```json
{
  "tokens": [
    { "text": "The", "part_of_speech": "DET", "dependency_edge": "DET", "lemma": "The" },
    { "text": "quick", "part_of_speech": "ADJ", "dependency_edge": "AMOD", "lemma": "quick" },
    { "text": "brown", "part_of_speech": "ADJ", "dependency_edge": "AMOD", "lemma": "brown" },
    { "text": "fox", "part_of_speech": "NOUN", "dependency_edge": "NSUBJ", "lemma": "fox" },
    { "text": "jumps", "part_of_speech": "VERB", "dependency_edge": "ROOT", "lemma": "jump" }
  ],
  "sentences": ["The quick brown fox jumps over the lazy dog."],
  "language": "en"
}
```

---

#### `POST /api/v1/nlp/classify` — Classify Content

Categorizes text into content categories. **The text must contain at least 20 words.**

**Request:**

```bash
curl -X POST http://localhost:8000/api/v1/nlp/classify \
  -H "X-API-Key: my-secret-key-1" \
  -F "text=Python is a versatile programming language used extensively in data science, machine learning, and web development. Its simple syntax and large ecosystem of libraries make it ideal for beginners and professionals alike."
```
```

**Response (200):**

```json
{
  "categories": [
    { "name": "/Computers & Electronics/Programming", "confidence": 0.89 },
    { "name": "/Science/Computer Science", "confidence": 0.72 }
  ]
}
```

---

## 🔐 Authentication & Rate Limiting Details

### Authentication: API Key

This application uses **API Key authentication** via the `X-API-Key` HTTP header.

| Aspect | Details |
|---|---|
| **Header Name** | `X-API-Key` |
| **Key Source** | Configured in `.env` via the `API_KEYS` variable |
| **Multiple Keys** | Supported — separate with commas |
| **Missing/Invalid Key** | Returns `401 Unauthorized` |

**How it works:**

1. Every request to `/api/v1/nlp/*` endpoints must include the `X-API-Key` header.
2. The server validates the key against the list of keys defined in the `API_KEYS` environment variable.
3. If the key is missing or invalid, the server responds with a `401 Unauthorized` error.

**Example error (missing key):**

```json
{
  "detail": "Missing API Key. Please provide a valid API key in the X-API-Key header."
}
```

### Rate Limiting

Rate limiting is implemented using **SlowAPI** to prevent abuse and ensure fair usage.

| Aspect | Details |
|---|---|
| **Default Limit** | 10 requests per minute |
| **Limit Scope** | Per API key (falls back to IP if no key) |
| **Configuration** | Set via `RATE_LIMIT` in `.env` |
| **Exceeded Response** | `429 Too Many Requests` |

**How it works:**

1. Each API key has its own rate counter.
2. When a request is made, the counter is incremented.
3. If the counter exceeds the configured limit within the time window, the server responds with `429`.
4. The counter resets automatically after the time window expires.

**Example rate limit formats:**

```
10/minute      # 10 requests per minute
100/hour       # 100 requests per hour
1000/day       # 1000 requests per day
```

---

## 🧪 Testing Instructions

### 1. Start the Server

```bash
python -m uvicorn app.main:app --reload
```

### 2. Test Health Check

```bash
curl http://localhost:8000/
```

Expected: `200 OK` with `"status": "healthy"`.

### 3. Test Authentication

**Missing API Key (expect 401):**

```bash
curl -X POST http://localhost:8000/api/v1/nlp/sentiment \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello world"}'
```

**Invalid API Key (expect 401):**

```bash
curl -X POST http://localhost:8000/api/v1/nlp/sentiment \
  -H "Content-Type: application/json" \
  -H "X-API-Key: invalid-key" \
  -d '{"text": "Hello world"}'
```

**Valid API Key (expect 200):**

```bash
curl -X POST http://localhost:8000/api/v1/nlp/sentiment \
  -H "Content-Type: application/json" \
  -H "X-API-Key: my-secret-key-1" \
  -d '{"text": "I love this product! It is amazing."}'
```

### 4. Test Rate Limiting

Send more than 10 requests within a minute to observe the `429 Too Many Requests` response:

```bash
# PowerShell: Rapid-fire 12 requests
for ($i = 1; $i -le 12; $i++) {
  Write-Host "Request $i :"
  curl -X POST http://localhost:8000/api/v1/nlp/sentiment `
    -H "Content-Type: application/json" `
    -H "X-API-Key: my-secret-key-1" `
    -d '{\"text\": \"Testing rate limiting.\"}'
  Write-Host ""
}
```

After 10 requests, subsequent ones should return `429`.

### 5. Test Using Swagger UI

Open `http://localhost:8000/docs` in your browser to test all endpoints interactively using the built-in Swagger UI. Click the **Authorize** button and enter your API key.

---

## 🔧 Troubleshooting Guide

| Problem | Cause | Solution |
|---|---|---|
| `401 Unauthorized` | Missing or invalid API key | Ensure `X-API-Key` header matches a key in your `.env` `API_KEYS` |
| `429 Too Many Requests` | Rate limit exceeded | Wait for the rate window to reset, or increase `RATE_LIMIT` in `.env` |
| `500 Internal Server Error` | Google Cloud credentials issue | Verify `GOOGLE_APPLICATION_CREDENTIALS` path is correct and the file exists |
| `502 Bad Gateway` | Google Cloud API error | Check that the Natural Language API is enabled in your GCP project |
| `400 Bad Request` on `/classify` | Text too short | Classification requires at least 20 words in the text |
| `ModuleNotFoundError` | Missing dependencies | Run `pip install -r requirements.txt` |
| Server won't start | Port in use | Change port: `uvicorn app.main:app --port 8001` |
| `.env` not loading | File not found | Ensure `.env` is in the project root directory (same level as `app/`) |

### Common Debug Steps

1. **Verify Google Cloud setup:**
   ```bash
   # Test if credentials are valid
   python -c "from google.cloud import language_v1; client = language_v1.LanguageServiceClient(); print('Credentials OK')"
   ```

2. **Check environment variables:**
   ```bash
   python -c "from app.config import get_settings; s = get_settings(); print(f'Keys: {s.api_keys_list}'); print(f'Rate: {s.RATE_LIMIT}')"
   ```

3. **Enable debug logging:**
   ```bash
   uvicorn app.main:app --reload --log-level debug
   ```

---

## 📁 Project Structure

```
Google Cloud Natural Language API/
├── app/
│   ├── __init__.py            # Package initializer
│   ├── main.py                # FastAPI application entry point
│   ├── config.py              # Environment configuration (pydantic-settings)
│   ├── auth.py                # API Key authentication dependency
│   ├── rate_limiter.py        # SlowAPI rate limiting setup
│   ├── models.py              # Pydantic request/response schemas
│   ├── nlp_service.py         # Google Cloud NLP API wrapper
│   └── routes/
│       ├── __init__.py        # Routes package initializer
│       └── nlp.py             # NLP endpoint definitions
├── .env                       # Environment variables (not in git)
├── .env.example               # Environment variable template
├── .gitignore                 # Git ignore rules
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

---

## 👥 Team Members and Contributions

| Name | Role | Contributions |
|---|---|---|
| *Member 1* | *Lead Developer* | *FastAPI setup, NLP service integration, endpoint development* |
| *Member 2* | *Security & DevOps* | *Authentication implementation, rate limiting, deployment configuration* |
| *Member 3* | *Documentation & Testing* | *README documentation, API testing, troubleshooting guide* |

> **Note:** Replace the placeholder names and contributions above with your actual team member information.

---

## 📄 License

This project was developed as part of **ITP 322 – Systems Integration and Architecture 2**.
