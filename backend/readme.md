#  Boundari AI Survey Generator

An AI-powered survey generation platform that transforms user descriptions into fully structured questionnaires using OpenAI's API. The system features intelligent caching, Docker containerization, and a modern React frontend.

---

## Features Implemented

### Core Features
- **AI-Powered Survey Generation** - Uses OpenAI API to generate contextual surveys from simple descriptions
- **Smart Caching System** - PostgreSQL database caches generated surveys to avoid redundant API calls
- **Professional UI** - Modal display generated surveys
- **Real-time Preview** - Instant visualization of questions, options, and rating scales

### Advanced Features
- **Full Docker Containerization** - Complete multi-container setup with Docker Compose
- **Token-based Authentication** - Secure API access with bearer token validation
- **Rate Limiting** - 3 requests per minute per token/IP to prevent abuse
- **Health Check Endpoints** - Container health monitoring for production readiness
- **CORS Configuration** - Flexible cross-origin resource sharing setup
- **Production-Ready Deployment** - Gunicorn + Nginx for optimal performance

---

## 🏗️ Architecture

```
┌─────────────────────────────────────┐
│  Frontend (React + TypeScript)      │
│  - Ask for Survey.                  │
│  - Survey display modal             │
│  Port: 80 (Nginx)                   │
└────────────┬────────────────────────┘
             │ HTTP Requests
             ↓
┌─────────────────────────────────────┐
│  Backend (Flask + Gunicorn)         │
│  - RESTful API endpoints            │
│  - OpenAI integration               │
│  - Token authentication             │
│  Port: 8000                         │
└────────────┬────────────────────────┘
             │ SQL Queries
             ↓
┌─────────────────────────────────────┐
│  PostgreSQL Database                │
│  - Survey caching                   │
│  - Persistent storage               │
│  Port: 5433 (mapped from 5432)      │
└─────────────────────────────────────┘
```

---

## Tech Stack

### Backend
- **Language:** Python 3.11
- **Framework:** Flask 3.1.1
- **Server:** Gunicorn (production WSGI server)
- **Database:** PostgreSQL 15
- **ORM:** SQLAlchemy 2.0
- **AI:** OpenAI API (GPT-4o-mini)
- **Authentication:** Bearer token validation
- **Rate Limiting:** Flask-Limiter

### Frontend
- **Framework:** React 19.1 + TypeScript
- **Styling:** Tailwind CSS
- **Animations:** Framer Motion
- **Server:** Nginx (production)
- **Build Tool:** React Scripts

### DevOps
- **Containerization:** Docker + Docker Compose
- **Images:** Multi-stage builds for optimized size
- **Networking:** Custom Docker network
- **Volumes:** Persistent PostgreSQL data

---

## rerequisites

- Docker Desktop installed and running
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))
- 2GB free disk space
- Ports 80, 8000, 5433 available

---

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/Toukir-Hasan/boundari-ai-backend
```

### 2. Configure Environment Variables

Create a `.env` file in the project root:

```env
# Database Configuration
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_secure_password
POSTGRES_DB=survey_db

# OpenAI Configuration
OPENAI_API_KEY=sk-your-openai-api-key-here

# API Authentication
SECRET_TOKEN=dev
```

### 3. Build and Start Services

```bash
# Build Docker images
docker-compose build

# Start all services
docker-compose up -d

# Check status
docker-compose ps
```

### 4. Initialize Database

```bash
docker-compose exec backend python -c "from app.db import engine; from app.models.survey import Base; Base.metadata.create_all(bind=engine); print(' Database initialized!')"
```

### 5. Access the Application

- **Frontend:** http://localhost
- **Backend API:** http://localhost:8000
- **Health Check:** http://localhost:8000/api/health

---

## Usage

### Generating a Survey

1. Open http://localhost in your browser
2. Click **"Generate Survey with AI"** button
3. Enter API token: `dev` (when prompted)
4. Enter survey description (e.g., "customer feedback survey")
5. Wait 2-3 seconds for AI generation
6. View the modal displaying your survey!



---

## API Endpoints

### Generate Survey

```http
POST /api/surveys/generate
Content-Type: application/json
Authorization: Bearer <SECRET_TOKEN>

{
  "prompt": "customer satisfaction survey"
}
```

**Response:**
```json
{
  "title": "Customer Satisfaction Survey",
  "questions": [
    {
      "type": "multiple_choice",
      "text": "How satisfied are you with our service?",
      "options": ["Very Satisfied", "Satisfied", "Neutral", "Dissatisfied"]
    },
    {
      "type": "rating",
      "text": "Rate your experience",
      "scale": 5
    }
  ]
}
```

### Health Check

```http
GET /api/health
```

**Response:**
```json
{
  "status": "healthy",
  "service": "boundari-backend"
}
```

---

## Database Schema

### Surveys Table

```sql
CREATE TABLE surveys (
    id SERIAL PRIMARY KEY,
    prompt_raw TEXT NOT NULL,
    prompt_normalized TEXT UNIQUE NOT NULL,
    survey_json JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Caching Strategy:**
- Prompts are normalized (lowercase, trimmed, whitespace collapsed)
- Duplicate prompts fetch from database instead of calling OpenAI
- Saves API costs and improves response time

---

## Docker Configuration

### Services

| Service | Image | Port | Purpose |
|---------|-------|------|---------|
| postgres | postgres:15-alpine | 5433:5432 | Database |
| backend | Custom (Python 3.11) | 8000:8000 | API Server |
| frontend | Custom (Node 18) | 80:80 | Web UI |

### Volumes

- `postgres_data` - Persistent database storage

### Networks

- `boundari-network` - Custom bridge network for inter-service communication

---

## Security Features

- ✅ Bearer token authentication on all API endpoints
- ✅ Rate limiting (3 requests/minute per token/IP)
- ✅ CORS configuration
- ✅ Security headers (X-Content-Type-Options, Referrer-Policy)
- ✅ Input validation (prompt length: 3-200 characters)
- ✅ SQL injection protection via SQLAlchemy ORM
- ✅ Environment variable secrets management

---

## Testing

### Test Backend Health

```bash
curl http://localhost:8000/api/health
```

### Test Survey Generation

```bash
curl -X POST http://localhost:8000/api/surveys/generate \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer dev" \
  -d '{"prompt":"employee feedback survey"}'
```

### Check Database

```bash
docker-compose exec postgres psql -U postgres -d survey_db -c "SELECT * FROM surveys;" -x
```

---

## Development Commands

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f postgres
```

### Restart Services

```bash
# All services
docker-compose restart

# Specific service
docker-compose restart backend
```

### Stop Services

```bash
docker-compose down
```

### Rebuild After Code Changes

```bash
# Backend changes
docker-compose build backend
docker-compose up -d

# Frontend changes
docker-compose build frontend
docker-compose up -d
```

---



## Project Structure

```
boundari-ai-backend/
├── backend/
│   ├── survey_service/
│   │   ├── app/
│   │   │   ├── config/        # Configuration
│   │   │   ├── models/        # SQLAlchemy models
│   │   │   ├── routes/        # API endpoints
│   │   │   └── tools/         # Utility scripts
│   │   ├── main.py            # Flask application
│   │   └── requirements.txt   # Python dependencies
│   ├── Dockerfile             # Backend container
│   └── .dockerignore          # Docker ignore rules
├── frontend/
│   ├── src/
│   │   ├── component/         # React components
│   │   └── pages/             # Page components
│   ├── public/                # Static assets
│   ├── Dockerfile             # Frontend container
│   ├── nginx.conf             # Nginx configuration
│   └── package.json           # Node dependencies
├── docker-compose.yml         # Multi-container orchestration
├── .env                       # Environment variables (not in git)
├── .env.example               # Environment template
└                # This file
```

---

## Key Implementation Highlights

### 1. Smart Caching System
- Normalized prompts prevent duplicate API calls
- Database-first approach for cost optimization
- Race condition handling with unique constraints

### 2. Beautiful Frontend Integration
- Custom modal component with Framer Motion animations
- Real-time survey preview with proper type handling
- localStorage integration for token persistence
- Responsive design for all screen sizes

### 3. Production-Ready Backend
- Gunicorn WSGI server with multiple workers
- Health check endpoints for monitoring
- Proper error handling and status codes
- Timeout configuration for long OpenAI responses

### 4. Docker Best Practices
- Multi-stage builds for smaller images
- Health checks for all services
- Dependency waiting (backend waits for DB)
- Volume persistence for data
- Custom networks for isolation

---



---

## 📝 Design Decisions

### Why Flask over FastAPI?
- Simpler for this scope
- More mature ecosystem
- Better documentation 
- Easier integration with existing tools

### Why Gunicorn?
- Production-grade WSGI server
- Better than Flask's built-in dev server
- Multiple workers for concurrency
- Timeout handling for long requests

### Why Multi-stage Docker Build for Frontend?
- Smaller final image (uses nginx:alpine)
- Build artifacts not included in production
- Faster deployment and startup

### Why PostgreSQL over MongoDB?
- ACID compliance for data integrity
- Better for relational data (surveys → questions)
- Excellent JSON support (JSONB type)
- More familiar to most developers

---

## Areas of Focus (Differentiators)

✨ **What makes this implementation stand out:**

1. **Complete Dockerization** - Production-ready multi-container setup
2. **Beautiful UI Integration** - Professional modal with animations
3. **Smart Caching** - Cost-optimized API usage
4. **Security First** - Token auth + rate limiting
5. **Health Monitoring** - Proper health check endpoints
6. **Production Server** - Gunicorn + Nginx stack
7. **Comprehensive Documentation** - Detailed README with examples

---

## 📚 Additional Resources

- [OpenAI API Documentation](https://platform.openai.com/docs/api-reference)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

---

## Contributing

This is a recruitment task project. Not accepting contributions.

---


## Acknowledgments

- Boundary AI for the challenge
- OpenAI for the API
- The open-source community

---

**Made with ❤️ using Docker, Flask, React, and OpenAI**
