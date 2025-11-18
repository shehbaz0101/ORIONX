# ORIONX Cloud Deployment Guide

This guide walks you through deploying ORIONX to the cloud using free-tier services.

## 🎯 Cloud Stack Overview

- **Backend (FastAPI)**: Railway.app
- **Frontend (Next.js)**: Vercel
- **Database (PostgreSQL + pgvector)**: Supabase
- **Cache (Redis)**: Upstash Redis
- **AI (DeepSeek R1)**: OpenRouter
- **Cron Jobs**: Railway Scheduled Jobs or Cron-job.org

---

## 📋 Prerequisites

1. GitHub account (for connecting repositories)
2. Railway account: https://railway.app
3. Vercel account: https://vercel.com
4. Supabase account: https://supabase.com
5. Upstash account: https://upstash.com
6. OpenRouter account: https://openrouter.ai

All services offer free tiers suitable for development and small-scale production.

---

## 🗄️ Step 1: Set Up Supabase Database

### 1.1 Create Supabase Project

1. Go to https://supabase.com and sign up/login
2. Click "New Project"
3. Choose an organization
4. Fill in:
   - **Name**: `orionx`
   - **Database Password**: Generate a strong password (save it!)
   - **Region**: Choose closest to your users
5. Click "Create new project" (takes ~2 minutes)

### 1.2 Run Database Migrations

1. In Supabase Dashboard, go to **SQL Editor**
2. Open each migration file from `supabase/migrations/` in order:
   - `001_enable_extensions.sql`
   - `002_create_users_table.sql`
   - `003_create_portfolios_table.sql`
   - `004_create_holdings_table.sql`
   - `005_create_news_articles_table.sql`
   - `006_create_filing_documents_table.sql`
   - `007_create_embedding_vectors_table.sql`
   - `008_create_screener_presets_table.sql`
   - `009_create_agent_task_logs_table.sql`
   - `010_create_price_data_table.sql`
3. Run each SQL file in sequence
4. Verify tables are created: Go to **Table Editor**

### 1.3 Get Database Connection String

1. Go to **Project Settings** > **Database**
2. Under **Connection string**, select **URI**
3. Copy the connection string
4. Replace `[YOUR-PASSWORD]` with your database password
5. Format: `postgresql+asyncpg://postgres:[PASSWORD]@db.[PROJECT_REF].supabase.co:5432/postgres`
6. Save this as `SUPABASE_DB_URL`

### 1.4 Get API Keys

1. Go to **Project Settings** > **API**
2. Copy:
   - **Project URL**: `https://[PROJECT_REF].supabase.co`
   - **anon/public key**: Save as `SUPABASE_ANON_KEY`
   - **service_role key**: Save as `SUPABASE_SERVICE_ROLE_KEY` (keep secret!)

---

## 🔴 Step 2: Set Up Upstash Redis

### 2.1 Create Redis Database

1. Go to https://upstash.com and sign up/login
2. Click "Create Database"
3. Fill in:
   - **Name**: `orionx-redis`
   - **Type**: Regional (free tier)
   - **Region**: Choose closest to your backend
4. Click "Create"

### 2.2 Get Redis Connection URL

1. In your database dashboard, click "REST API" tab
2. Copy the **Redis URL**
3. Format: `redis://default:[PASSWORD]@[ENDPOINT].upstash.io:[PORT]`
4. Save this as `UPSTASH_REDIS_URL`

---

## 🤖 Step 3: Set Up OpenRouter (AI)

1. Go to https://openrouter.ai and sign up/login
2. Go to **Keys** section
3. Click "Create Key"
4. Copy the API key (starts with `sk-or-v1-`)
5. Save this as `OPENROUTER_API_KEY`

---

## 🚂 Step 4: Deploy Backend to Railway

### 4.1 Connect Repository

1. Go to https://railway.app and sign up/login
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Authorize Railway to access your GitHub
5. Select the `ORIONX` repository
6. Railway will detect the backend automatically

### 4.2 Configure Environment Variables

1. In Railway project, click on your service
2. Go to **Variables** tab
3. Add the following variables:

```bash
SUPABASE_DB_URL=postgresql+asyncpg://postgres:[PASSWORD]@db.[PROJECT_REF].supabase.co:5432/postgres
UPSTASH_REDIS_URL=redis://default:[PASSWORD]@[ENDPOINT].upstash.io:[PORT]
OPENROUTER_API_KEY=sk-or-v1-[YOUR_KEY]
SECRET_KEY=[GENERATE_RANDOM_SECRET_FOR_JWT]
FRONTEND_DOMAIN=app.orionx.ai  # Optional: your custom domain
```

**Generate SECRET_KEY:**
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 4.3 Configure Build Settings

1. Railway should auto-detect Python
2. Ensure **Root Directory** is set to `backend/`
3. Railway will use the `Procfile` automatically
4. If needed, set **Start Command**: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`

### 4.4 Deploy

1. Railway will automatically deploy on push to main branch
2. Check **Deployments** tab for build logs
3. Once deployed, Railway provides a public URL like: `https://[APP_NAME].railway.app`
4. Test: Visit `https://[APP_NAME].railway.app/health`

### 4.5 Get Backend URL

1. In Railway, go to your service
2. Click **Settings** > **Domains**
3. Copy the **Public Domain** (or set a custom domain)
4. Save this URL as your backend API URL

---

## ⚡ Step 5: Deploy Frontend to Vercel

### 5.1 Connect Repository

1. Go to https://vercel.com and sign up/login
2. Click "Add New" > "Project"
3. Import your GitHub repository
4. Select the `ORIONX` repository

### 5.2 Configure Build Settings

1. **Framework Preset**: Next.js (auto-detected)
2. **Root Directory**: `frontend/`
3. **Build Command**: `npm run build` (default)
4. **Output Directory**: `.next` (default)
5. **Install Command**: `npm install` (default)

### 5.3 Configure Environment Variables

1. In project settings, go to **Environment Variables**
2. Add the following:

```bash
NEXT_PUBLIC_API_URL=https://[YOUR_RAILWAY_APP].railway.app
NEXT_PUBLIC_WS_URL=wss://[YOUR_RAILWAY_APP].railway.app
NEXT_PUBLIC_SUPABASE_URL=https://[PROJECT_REF].supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=[YOUR_SUPABASE_ANON_KEY]
```

**Important**: 
- `NEXT_PUBLIC_*` variables are exposed to the browser
- Use `wss://` (secure WebSocket) for production
- Railway URL should match your backend deployment

### 5.4 Deploy

1. Click "Deploy"
2. Vercel will build and deploy automatically
3. Once deployed, you'll get a URL like: `https://[PROJECT_NAME].vercel.app`
4. Test: Visit the URL and check if frontend loads

### 5.5 Update Backend CORS

1. Go back to Railway backend environment variables
2. Add/update:
   ```bash
   VERCEL_URL=[YOUR_VERCEL_PROJECT].vercel.app
   FRONTEND_DOMAIN=app.orionx.ai  # If using custom domain
   ```
3. Redeploy backend (Railway auto-redeploys on env var changes)

---

## 🔗 Step 6: Connect Frontend ↔ Backend

### 6.1 Verify CORS

1. Open browser DevTools (F12)
2. Go to **Network** tab
3. Try logging in or making an API call
4. Check for CORS errors in console
5. If errors, verify backend CORS configuration includes your Vercel URL

### 6.2 Test WebSocket Connection

1. Open browser DevTools > **Console**
2. Navigate to a page using WebSocket (e.g., Markets page)
3. Check for WebSocket connection logs
4. Verify `wss://` is used (not `ws://`) for production

---

## 🌐 Step 7: Set Up Custom Domain (Optional)

### 7.1 Backend Domain (Railway)

1. In Railway, go to **Settings** > **Domains**
2. Click "Generate Domain" or "Add Custom Domain"
3. For custom domain: `api.orionx.ai`
4. Add DNS records as instructed by Railway
5. Update `NEXT_PUBLIC_API_URL` in Vercel to use custom domain

### 7.2 Frontend Domain (Vercel)

1. In Vercel, go to **Settings** > **Domains**
2. Add your domain: `app.orionx.ai`
3. Add DNS records as instructed by Vercel
4. Update `FRONTEND_DOMAIN` in Railway backend env vars

---

## ⏰ Step 8: Set Up Cron Jobs

### Option A: Railway Scheduled Jobs

1. In Railway, create a new service
2. Select "Empty Service"
3. Add a **Cron** trigger:
   - **Schedule**: `0 9 * * *` (9 AM daily)
   - **Command**: `python -m backend.ai_agents.runner`
4. Add same environment variables as backend
5. Deploy

### Option B: Cron-job.org (Free)

1. Go to https://cron-job.org
2. Create account
3. Create new cron job:
   - **URL**: `https://[YOUR_RAILWAY_APP].railway.app/api/agents/run`
   - **Schedule**: Daily at 9 AM
   - **Method**: POST
4. Add authentication header if needed

---

## ✅ Step 9: Verify Deployment

### Backend Health Check

```bash
curl https://[YOUR_RAILWAY_APP].railway.app/health
```

Expected response:
```json
{"status": "healthy", "service": "ORIONX"}
```

### Frontend Check

1. Visit your Vercel URL
2. Try registering/logging in
3. Test key features:
   - Market data
   - Portfolio creation
   - News feed
   - AI copilot

### Database Check

1. In Supabase Dashboard > **Table Editor**
2. Verify tables exist
3. Try creating a user via frontend
4. Check if user appears in `users` table

### Redis Check

1. In Upstash Dashboard
2. Go to **Console** tab
3. Run: `PING`
4. Should return: `PONG`

---

## 🔧 Troubleshooting

### Backend Issues

**Problem**: Backend won't start
- Check Railway logs: **Deployments** > **View Logs**
- Verify all environment variables are set
- Check `SUPABASE_DB_URL` format (must include `+asyncpg`)

**Problem**: Database connection fails
- Verify `SUPABASE_DB_URL` is correct
- Check Supabase database is running
- Verify password is correct

**Problem**: Redis connection fails
- Verify `UPSTASH_REDIS_URL` format
- Check Upstash database is active
- Test connection in Upstash Console

### Frontend Issues

**Problem**: CORS errors
- Verify `NEXT_PUBLIC_API_URL` is correct
- Check backend CORS includes Vercel domain
- Ensure `VERCEL_URL` is set in Railway

**Problem**: API calls fail
- Check `NEXT_PUBLIC_API_URL` in Vercel env vars
- Verify backend is deployed and healthy
- Check browser console for errors

**Problem**: WebSocket fails
- Ensure `NEXT_PUBLIC_WS_URL` uses `wss://` (not `ws://`)
- Verify Railway supports WebSocket (it does by default)
- Check backend WebSocket endpoint is accessible

### Database Issues

**Problem**: Migrations fail
- Run migrations one at a time in Supabase SQL Editor
- Check for syntax errors
- Verify pgvector extension is enabled

**Problem**: Tables missing
- Re-run migrations in order
- Check Supabase logs for errors

---

## 📊 Monitoring & Maintenance

### Railway Monitoring

1. Go to Railway Dashboard
2. Check **Metrics** tab for:
   - CPU usage
   - Memory usage
   - Request count
3. Set up alerts for high usage

### Vercel Analytics

1. Enable Vercel Analytics in project settings
2. Monitor:
   - Page views
   - Performance metrics
   - Error rates

### Supabase Monitoring

1. Go to Supabase Dashboard > **Database** > **Connection Pooling**
2. Monitor:
   - Active connections
   - Query performance
   - Database size

### Upstash Monitoring

1. Go to Upstash Dashboard
2. Check:
   - Request count
   - Data transfer
   - Memory usage

---

## 🔐 Security Checklist

- [ ] All secrets are in environment variables (not in code)
- [ ] `SECRET_KEY` is strong and random
- [ ] `SUPABASE_SERVICE_ROLE_KEY` is kept secret (backend only)
- [ ] CORS is configured correctly (not `allow_origins=["*"]`)
- [ ] HTTPS is enabled (automatic on Railway/Vercel)
- [ ] Database password is strong
- [ ] Redis password is secure
- [ ] API keys are rotated regularly

---

## 🚀 Next Steps

1. **Enable Analytics**: Set up Vercel Analytics and Railway monitoring
2. **Set Up CI/CD**: Configure automatic deployments on git push
3. **Add Custom Domain**: Configure `app.orionx.ai` and `api.orionx.ai`
4. **Set Up Backups**: Configure Supabase backups
5. **Monitor Costs**: Track usage to stay within free tiers
6. **Scale Up**: Upgrade to paid tiers when needed

---

## 📞 Support

- Railway Docs: https://docs.railway.app
- Vercel Docs: https://vercel.com/docs
- Supabase Docs: https://supabase.com/docs
- Upstash Docs: https://docs.upstash.com

---

## 🎉 Success!

Your ORIONX application is now fully deployed to the cloud! 🚀

Visit your Vercel URL to start using the application.

