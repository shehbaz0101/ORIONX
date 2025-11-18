# ORIONX

AI-powered Bloomberg Terminal alternative built with FastAPI, Next.js, PostgreSQL, and pgvector.

## Features

- **Real-Time Market Data**: Live equity, crypto, and FX data via WebSockets
- **AI Copilot**: DeepSeek R1-powered assistant with tool calling
- **Portfolio Analytics**: PnL tracking, exposure analysis, risk metrics
- **News & Sentiment**: RSS ingestion with AI-powered sentiment analysis
- **SEC Filings RAG**: Semantic search in SEC filings using pgvector
- **Risk Engine**: Volatility, correlation, VaR calculations
- **Stock Screener**: Technical and fundamental screening with NLP
- **Scenario Simulation**: Rate shocks, FX shocks, volatility scenarios
- **9 AI Agents**: Automated monitoring and analysis agents

## Tech Stack

### Backend
- FastAPI (Python 3.11+)
- PostgreSQL with pgvector
- Redis for caching
- WebSockets for real-time data
- APScheduler for agent scheduling

### Frontend
- Next.js 15 (App Router)
- React 18
- TailwindCSS
- Framer Motion
- Stripe-style UI design

### AI/ML
- DeepSeek R1 via OpenRouter
- pgvector for embeddings
- Tool calling system

## Architecture

```
ORIONX
├── backend/
│   ├── main.py              # FastAPI app
│   ├── api.py               # Router aggregation
│   ├── db/                  # Database models & setup
│   ├── auth/                # Authentication
│   ├── market_data/         # Real-time & historical data
│   ├── news/                # RSS ingestion & sentiment
│   ├── filings_rag/         # EDGAR + embeddings
│   ├── portfolio/           # Portfolio management
│   ├── risk/                # Risk engine
│   ├── screener/            # Stock screener
│   ├── scenario/            # Scenario simulation
│   ├── ai_copilot/          # AI Copilot service
│   └── ai_agents/           # 9 AI agents
└── frontend/
    ├── app/                 # Next.js pages
    ├── components/          # React components
    └── lib/                  # Utilities
```

## 🚀 Cloud Deployment (Recommended)

ORIONX is designed for cloud deployment using free-tier services:

- **Backend**: Railway.app (FastAPI)
- **Frontend**: Vercel (Next.js)
- **Database**: Supabase (PostgreSQL + pgvector)
- **Cache**: Upstash Redis
- **AI**: OpenRouter (DeepSeek R1)

**👉 See [CLOUD_DEPLOYMENT_GUIDE.md](./CLOUD_DEPLOYMENT_GUIDE.md) for complete deployment instructions.**

### Quick Start (Cloud)

1. **Set up Supabase**: Create project and run migrations from `supabase/migrations/`
2. **Set up Upstash Redis**: Create database and get connection URL
3. **Deploy Backend to Railway**: Connect GitHub repo, set environment variables
4. **Deploy Frontend to Vercel**: Connect GitHub repo, set environment variables
5. **Configure**: Update CORS and connect frontend ↔ backend

See `env.example.cloud` for all required environment variables.

---

## 💻 Local Development

### Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL 16+ (with pgvector extension)
- Redis 7+

### Environment Variables

Copy `.env.example.cloud` and configure for local development:

```bash
# Local PostgreSQL
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/orionx

# Local Redis
REDIS_URL=redis://localhost:6379/0

# Required
SECRET_KEY=your-secret-key
OPENROUTER_API_KEY=your-openrouter-api-key
```

### Local Setup

#### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Initialize database (creates tables and extensions)
# Make sure PostgreSQL is running with pgvector extension
uvicorn backend.main:app --reload
```

#### Frontend

```bash
cd frontend
npm install

# Set environment variable
export NEXT_PUBLIC_API_URL=http://localhost:8000  # Linux/Mac
# or
set NEXT_PUBLIC_API_URL=http://localhost:8000  # Windows

npm run dev
```

#### Database Setup (Local)

1. Install PostgreSQL with pgvector extension
2. Create database: `createdb orionx`
3. Enable extension: `psql orionx -c "CREATE EXTENSION vector;"`
4. Run migrations from `supabase/migrations/` or let the app auto-create tables

**Note**: For cloud deployment, use Supabase migrations. For local dev, tables are auto-created via SQLAlchemy.

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register user
- `POST /api/auth/login` - Login

### Market Data
- `GET /api/market/history` - Historical data
- `GET /api/market/fundamentals` - Fundamentals
- `GET /api/market/metadata` - Company metadata
- `GET /api/market/fx/rate` - FX rates
- `WebSocket /api/market/ws` - Real-time data

### News
- `GET /api/news/feed` - News feed
- `GET /api/news/search` - Search news
- `POST /api/news/sync` - Sync RSS feeds

### Filings
- `POST /api/filings/sync` - Sync SEC filings
- `GET /api/filings/search` - Semantic search

### Portfolio
- `POST /api/portfolio/create` - Create portfolio
- `POST /api/portfolio/upload` - Upload holdings CSV
- `GET /api/portfolio/valuation` - Get valuation

### Risk
- `GET /api/risk/overview` - Risk overview

### Screener
- `POST /api/screener/run` - Run screener
- `POST /api/screener/nlp` - NLP screener

### Scenario
- `POST /api/scenario/simulate` - Run scenario

### AI
- `POST /api/ai/copilot` - Chat with AI Copilot

## AI Agents

1. **Morning Briefing Agent** - Daily market summary (8 AM)
2. **Real-Time Drawdown Watcher** - Monitor portfolio drawdowns
3. **PnL Explanation Agent** - Explain portfolio performance
4. **Earnings Week Agent** - Track earnings (9 AM)
5. **SEC Filing Intelligence Agent** - Monitor filings (10 AM)
6. **News Sentiment Agent** - Analyze sentiment (every 4 hours)
7. **Risk Sentinel Agent** - Monitor risk metrics
8. **Screener Intelligence Agent** - Build smart screeners
9. **Scenario Simulation Agent** - Run scenario analyses

## Data Sources (Free)

- **Equities**: Alpaca Market Data WebSocket (public feed)
- **Crypto**: Binance public WebSocket
- **FX**: exchangerate.host API
- **Historical**: yfinance
- **Fundamentals**: yfinance
- **News**: Yahoo Finance RSS, CNBC RSS, MarketWatch RSS
- **Filings**: SEC EDGAR

## 📦 Project Structure

```
ORIONX/
├── backend/              # FastAPI backend
│   ├── main.py          # Application entry point
│   ├── Procfile         # Railway deployment config
│   ├── railway.json     # Railway service config
│   └── ...
├── frontend/            # Next.js frontend
│   ├── vercel.json      # Vercel deployment config
│   └── ...
├── supabase/
│   └── migrations/      # Database migration SQL files
├── env.example.cloud     # Cloud environment variables template
└── CLOUD_DEPLOYMENT_GUIDE.md  # Complete deployment guide
```

## 🔧 Configuration

### Environment Variables

See `.env.example.cloud` for all required variables:

**Backend (Railway):**
- `SUPABASE_DB_URL` - Supabase PostgreSQL connection string
- `UPSTASH_REDIS_URL` - Upstash Redis connection URL
- `OPENROUTER_API_KEY` - OpenRouter API key
- `SECRET_KEY` - JWT secret key
- `FRONTEND_DOMAIN` - Frontend domain for CORS (optional)

**Frontend (Vercel):**
- `NEXT_PUBLIC_API_URL` - Railway backend URL
- `NEXT_PUBLIC_WS_URL` - WebSocket URL (wss:// for production)
- `NEXT_PUBLIC_SUPABASE_URL` - Supabase project URL
- `NEXT_PUBLIC_SUPABASE_ANON_KEY` - Supabase anonymous key

## 🚢 Production Deployment

ORIONX is fully cloud-deployable. Follow the [Cloud Deployment Guide](./CLOUD_DEPLOYMENT_GUIDE.md) for step-by-step instructions.

**Key Points:**
- ✅ All services use free tiers
- ✅ Zero local dependencies
- ✅ Automatic HTTPS/SSL
- ✅ Auto-scaling on Railway/Vercel
- ✅ Database migrations via Supabase SQL Editor

## License

MIT

## Contributing

Contributions welcome! Please open an issue or PR.
