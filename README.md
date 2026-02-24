# 🎯 SkillSwap Matching Service

**Specialized AI microservice** for intelligent skill matching using semantic similarity and exact matching algorithms.

> **Note:** This is a standalone microservice designed to be called by the main SkillSwap Node.js/Express backend. It handles computationally intensive AI-powered matching operations.

## 🚀 Features

- **Hybrid Matching Algorithm**: Combines exact string matching with AI-powered semantic similarity
- **Vector Embeddings**: Uses Sentence Transformers (all-MiniLM-L6-v2) for 384-dimensional skill embeddings
- **High Performance**: Async FastAPI with PostgreSQL connection pooling and Redis caching
- **Scalable**: Docker-ready with pgvector for efficient similarity searches
- **Smart Scoring**: Weighted algorithm (60% what you get, 40% what you give)

## 🏗️ Architecture

### Microservice Architecture
```
┌─────────────────────┐
│  Node.js Backend    │  ← Main application (auth, CRUD, business logic)
│  (Port 3000/4000)   │
└──────────┬──────────┘
           │ HTTP calls
           ▼
┌─────────────────────┐
│  FastAPI Service    │  ← This microservice (AI matching)
│  (Port 8001)        │
└──────────┬──────────┘
           │
           ▼
  PostgreSQL (Shared) + Redis Cache
           │
           ▼
  Sentence Transformers (AI Model)
```

### Integration
The Node.js backend calls this service via HTTP:
```javascript
// Example: Node.js calling this service
const matches = await axios.post(
  'https://skillswap-matching-service.onrender.com/api/matches/user123',
  { limit: 10 }
);
```

## 📋 Prerequisites

- Python 3.11+
- PostgreSQL with pgvector extension
- Redis (Upstash recommended)
- Docker (optional)

## ⚙️ Installation

### Local Development

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ispastro/skillswap_matching_service.git
   cd skillswap_matching_service
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your credentials
   ```

5. **Run the service:**
   ```bash
   uvicorn app.main:app --reload --port 8001
   ```

### Docker Deployment

```bash
docker-compose up --build
```

## 🔧 Configuration

Required environment variables in `.env`:

```env
DATABASE_URL=postgresql://user:pass@host:5432/db
REDIS_UPSTASH_REST_URL=https://your-redis.upstash.io
REDIS_UPSTASH_REST_TOKEN=your_token
```

## 📡 API Endpoints

### Core Endpoint

**POST** `/api/matches/{user_id}`

Find best skill matches for a user.

**Query Parameters:**
- `limit` (optional): Max matches to return (default: 10)

**Response:**
```json
{
  "user_id": "123",
  "username": "alice",
  "total_matches": 5,
  "matches": [
    {
      "user_id": "456",
      "username": "bob",
      "score": 85.5,
      "what_i_get": {
        "exact": ["Python", "Django"],
        "semantic": [
          {"skill": "Machine Learning", "matched_with": "Deep Learning", "similarity": 0.78}
        ]
      },
      "what_i_give": {
        "exact": ["React"],
        "semantic": []
      }
    }
  ]
}
```

### Health & Debug

- `GET /health` - Service health check
- `GET /` - Welcome message
- `GET /db-test` - Database connectivity
- `GET /embedding-test` - AI model test
- `GET /similarity-test` - Semantic similarity demo

## 🧠 Matching Algorithm

### Phase 1: Exact Matching
Case-insensitive string comparison for direct skill matches.

### Phase 2: Semantic Matching
- Generates 384-dimensional embeddings using Sentence Transformers
- Calculates cosine similarity between skill vectors
- Matches skills with ≥50% similarity threshold

### Scoring Formula
```
score = (matches_i_get / skills_i_want × 60) + (matches_i_give / skills_they_want × 40)
```

## 🗄️ Database Schema

### User Table
```sql
CREATE TABLE "User" (
  id TEXT PRIMARY KEY,
  username VARCHAR,
  email VARCHAR,
  skillsWant TEXT[],
  skillsHave TEXT[],
  ...
);
```

### SkillEmbedding Table
```sql
CREATE TABLE "SkillEmbedding" (
  id TEXT PRIMARY KEY,
  skill VARCHAR,
  embedding vector(384),
  ...
);
```

## 🔗 Integration with Node.js Backend

This service is designed to be called by your main Node.js/Express backend:

### Node.js Example:
```javascript
const axios = require('axios');

const MATCHING_SERVICE_URL = process.env.MATCHING_SERVICE_URL || 'https://skillswap-matching-service.onrender.com';

// Get matches for a user
app.get('/api/users/:userId/matches', async (req, res) => {
  try {
    const response = await axios.post(
      `${MATCHING_SERVICE_URL}/api/matches/${req.params.userId}`,
      { params: { limit: req.query.limit || 10 } }
    );
    res.json(response.data);
  } catch (error) {
    console.error('Matching service error:', error);
    res.status(503).json({ error: 'Matching service unavailable' });
  }
});
```

### Environment Variables (Node.js):
```env
MATCHING_SERVICE_URL=https://skillswap-matching-service.onrender.com
```

## 🚀 Deployment

See [DEPLOY.md](DEPLOY.md) for Render deployment instructions.

### ⚠️ Render Free Tier: Preventing Sleep
Render free tier spins down after 15 minutes. See [KEEP_ALIVE.md](KEEP_ALIVE.md) for solutions to keep your service awake 24/7 (completely free).

## 🧪 Testing

```bash
# Run tests (when implemented)
pytest

# Test endpoints locally
curl http://localhost:8001/health
curl -X POST http://localhost:8001/api/matches/user123?limit=5
```

## 📊 Performance

- **Caching**: 5-minute TTL on match results
- **Connection Pool**: 10 connections, 20 max overflow
- **Async I/O**: Non-blocking database operations
- **Batch Processing**: Multiple embeddings generated in single model call

## 🔒 Security Notes

- All credentials stored as environment variables
- Never commit `.env` file
- Use Render's encrypted secrets for production
- TODO: Add authentication/authorization

## 🛠️ Tech Stack

- **Framework**: FastAPI 0.115+
- **Database**: PostgreSQL + pgvector
- **Cache**: Upstash Redis
- **AI/ML**: Sentence Transformers (all-MiniLM-L6-v2)
- **ORM**: SQLAlchemy 2.0 (async)
- **Deployment**: Docker + Render

## 📝 License

MIT

## 👤 Author

**Haile** ([@ispastro](https://github.com/ispastro))

Built with ❤️ for SkillSwap Platform
