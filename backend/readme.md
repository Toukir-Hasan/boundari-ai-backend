## Architecture & Design

**Structure**

backend/
└── survey_service/
├── app/
│ ├── config/ # Centralized configuration (reads from .env)
│ ├── models/ # SQLAlchemy ORM models
│ ├── routes/ # Route blueprints (e.g., generate.py)
│ ├── tools/ # DB initialization scripts
│ ├── db.py # Database session handling
│ ├── auth.py # Token authentication utilities
│ └── init.py # App factory
├── requirements.txt
├── Dockerfile (future use)
└── main.py

**Design choices**
- **Flask** was chosen over FastAPI for simplicity and faster onboarding.
- **Blueprints** keep routes modular and maintainable.
- **Config Management** via `.env` + `python-dotenv`, allowing easy switching between local and cloud databases.
- **SQLAlchemy ORM** for DB abstraction and portability.
- **PostgreSQL** as the relational store; Azure DB-ready.

---

## Tech Stack

| Layer               | Technology                       | Rationale                                                                 |
|---------------------|-----------------------------------|---------------------------------------------------------------------------|
| Backend Framework   | Flask                            | Lightweight, proven, and easy to integrate with existing Python stack.   |
| Database ORM        | SQLAlchemy                       | ORM with clean session management and migrations support.                |
| Database            | PostgreSQL                       | Reliable, production-grade relational DB.                                |
| API Client          | `openai` (>=1.0.0)               | Official SDK for AI-powered survey generation.                           |
| Auth & Security     | Custom Bearer token + Flask-Limiter | Lightweight, simple to extend with real auth.                            |
| Config Management   | `python-dotenv`                  | Centralized environment variable handling.                               |

---

## API Design

### Endpoint
`POST /api/surveys/generate`

**Request**
```json
{
  "prompt": "Customer feedback survey for a coffee shop"
}


{
  "title": "Customer Feedback Survey",
  "questions": [
    {
      "type": "rating",
      "text": "How satisfied are you with our coffee?",
      "scale": 5
    },
    {
      "type": "open_text",
      "text": "What can we improve?"
    }
  ]
}
```

## Error Responses

- **400 Bad Request** — Invalid or missing prompt

- **401 Unauthorized** — Missing or incorrect API token

- **502 Bad Gateway** — AI output not in valid JSON

- **500 Internal Server Error** — Unexpected server/database errors

## Integration & Robustness

- **Authentication:** Simple Bearer token check from Authorization header.

- **Rate Limiting:** Configurable (e.g., 3 requests/minute per client) via Flask-Limiter.

- **Input Validation:** Prompt length (3–200 chars), JSON content type enforced.

- **Error Handling:** Graceful handling of OpenAI errors, DB errors, and schema validation.

- **Caching:** Duplicate prompts (case/whitespace-insensitive) served from DB without re-calling OpenAI.

- **Timeouts:** OpenAI API calls can be configured with request timeouts.

## Performance & Security
- **Cold Start Optimization:** Minimal imports in route functions, app factory pattern for reuse.

- **Input Sanitization:** Normalization of prompt before DB insertion to prevent injection.

- **Minimal Attack Surface:** Only one public POST endpoint, token-protected.

## Setup & Run Instructions

- git clone

## Create Virtual Environment inside the survey_service

- python -m venv venv
- source venv/bin/activate  
- venv\Scripts\activate  

## Install Dependencies
- pip install -r requirements.txt

# Configure Environment Variables
- OPENAI_API_KEY=sk-xxxx
- SECRET_TOKEN=your-very-secret-token
- DATABASE_URL=postgresql://<user>:<pass>@localhost:5432/surveydb

## Initialize Database
- python app/tools/init_db.py

## Run Server
- python main.py


## Areas of Focus / Bonus Features
- Authentication

- Simple Bearer token validation ensures only authorized clients can access the endpoint.

- Rate Limiting

- Prevents abuse by limiting requests per minute per client IP.

- Security

- Input validation, token-based auth, and minimal exposed surface reduce vulnerability.

- Secrets loaded from environment, never hardcoded.

- Caching

- Avoids duplicate OpenAI calls for the same prompt, improving performance and reducing cost.

## Future Enhancements

- Replace simple token auth with JWT/OAuth2.

- Deploy behind Nginx with HTTPS.

- Add integration tests.

- Dockerize for portable deployment.

- Implement async for OpenAI calls to improve concurrency.
