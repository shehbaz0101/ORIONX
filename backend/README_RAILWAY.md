# ORIONX Backend - Railway Deployment

This backend is configured for Railway.app deployment.

## Quick Start

1. Set Root Directory to: `backend`
2. Add environment variables (see Railway deployment guide)
3. Deploy!

## Files

- `Procfile` - Railway process file
- `railway.json` - Railway service configuration
- `requirements.txt` - Python dependencies
- `main.py` - FastAPI application entry point

## Environment Variables Required

- `SUPABASE_DB_URL` - Supabase PostgreSQL connection
- `UPSTASH_REDIS_URL` - Upstash Redis connection
- `OPENROUTER_API_KEY` - OpenRouter API key
- `SECRET_KEY` - JWT secret key
- `PORT` - Automatically set by Railway

## Health Check

After deployment, test:
- Health: `GET /health`
- Docs: `GET /docs`
- Root: `GET /`

