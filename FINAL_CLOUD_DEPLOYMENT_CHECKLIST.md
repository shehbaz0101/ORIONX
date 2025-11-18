# 🚀 ORIONX - FINAL CLOUD DEPLOYMENT CHECKLIST

Complete step-by-step guide to deploy ORIONX to production using free-tier cloud services.

---

## 📋 PRE-DEPLOYMENT CHECKLIST

Before starting, ensure you have:
- [ ] GitHub account with ORIONX repository
- [ ] Supabase account (free tier)
- [ ] Railway account (free tier)
- [ ] Vercel account (free tier)
- [ ] Upstash account (free tier)
- [ ] OpenRouter account (free tier)

---

## 🗄️ STEP 1: SET UP SUPABASE DATABASE

### 1.1 Create Supabase Project

1. Go to **https://supabase.com/dashboard**
2. Click **"New Project"**
3. Fill in:
   - **Name**: `orionx`
   - **Database Password**: Generate strong password (SAVE IT!)
   - **Region**: Choose closest to your users
4. Click **"Create new project"** (takes ~2 minutes)

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
4. Verify: Go to **Table Editor** - all 9 tables should exist

### 1.3 Get Supabase Credentials

1. Go to **Project Settings** > **API**
2. Copy these values (you'll need them):
   - **Project URL**: `https://[PROJECT_REF].supabase.co` → `SUPABASE_URL`
   - **anon/public key** → `SUPABASE_ANON_KEY`
   - **service_role key** → `SUPABASE_SERVICE_ROLE_KEY` (KEEP SECRET!)

3. Go to **Project Settings** > **Database**
4. Under **Connection string**, select **URI**
5. Copy the connection string
6. Replace `[YOUR-PASSWORD]` with your database password
7. Replace `postgresql://` with `postgresql+asyncpg://`
8. Add `?sslmode=require` at the end
9. This is your `SUPABASE_DB_URL`

**Example format:**
```
postgresql+asyncpg://postgres:[PASSWORD]@db.[PROJECT_REF].supabase.co:5432/postgres?sslmode=require
```

### 1.4 Verify Database

Run this SQL in Supabase SQL Editor:
```sql
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public' 
  AND table_type = 'BASE TABLE'
ORDER BY table_name;
```

**Expected tables:**
- agent_task_logs
- embedding_vectors
- filing_documents
- holdings
- news_articles
- portfolios
- price_data
- screener_presets
- users

---

## 🔴 STEP 2: SET UP UPSTASH REDIS

### 2.1 Create Redis Database

1. Go to **https://console.upstash.com**
2. Click **"Create Database"**
3. Fill in:
   - **Name**: `orionx-redis`
   - **Type**: Regional (free tier)
   - **Region**: Choose closest to your backend
4. Click **"Create"**

### 2.2 Get Redis Connection URL

1. In your database dashboard, click **"REST API"** tab
2. Copy the **Redis URL**
3. Format: `redis://default:[PASSWORD]@[ENDPOINT].upstash.io:[PORT]`
4. This is your `REDIS_URL`

---

## 🤖 STEP 3: SET UP OPENROUTER (AI)

1. Go to **https://openrouter.ai/keys**
2. Click **"Create Key"**
3. Copy the API key (starts with `sk-or-v1-`)
4. This is your `OPENROUTER_API_KEY`

---

## 🚂 STEP 4: DEPLOY BACKEND TO RAILWAY

### 4.1 Create Railway Project

1. Go to **https://railway.app**
2. Click **"New Project"** (top right)
3. Select **"Deploy from GitHub repo"**
4. Authorize Railway to access GitHub (if first time)
5. Select your **ORIONX** repository
6. Railway will auto-detect it's a Python project

### 4.2 Configure Service Settings

1. Click on the service (likely named after your repo)
2. Go to **Settings** tab
3. **IMPORTANT**: Set **Root Directory** to: `backend`
4. Click **"Save"**

### 4.3 Add Environment Variables

Go to **Variables** tab and click **"New Variable"** for each:

#### Variable 1: SUPABASE_DB_URL
- **Name**: `SUPABASE_DB_URL`
- **Value**: `postgresql+asyncpg://postgres:[YOUR_PASSWORD]@db.[PROJECT_REF].supabase.co:5432/postgres?sslmode=require`
- Click **"Add"**

#### Variable 2: SUPABASE_SERVICE_ROLE_KEY
- **Name**: `SUPABASE_SERVICE_ROLE_KEY`
- **Value**: `[YOUR_SERVICE_ROLE_KEY]` (from Supabase)
- Click **"Add"**

#### Variable 3: REDIS_URL
- **Name**: `REDIS_URL`
- **Value**: `redis://default:[PASSWORD]@[ENDPOINT].upstash.io:[PORT]` (from Upstash)
- Click **"Add"**

#### Variable 4: OPENROUTER_API_KEY
- **Name**: `OPENROUTER_API_KEY`
- **Value**: `sk-or-v1-[YOUR_KEY]` (from OpenRouter)
- Click **"Add"**

#### Variable 5: SECRET_KEY
- **Name**: `SECRET_KEY`
- **Value**: Generate with: `python -c "import secrets; print(secrets.token_urlsafe(32))"`
- Click **"Add"**

#### Variable 6: CORS_ORIGINS
- **Name**: `CORS_ORIGINS`
- **Value**: `*`
- Click **"Add"**

**Note**: Railway automatically provides `PORT` - do NOT set it manually.

### 4.4 Deploy

1. Railway will automatically start deploying
2. Go to **Deployments** tab
3. Watch the build logs
4. Wait for deployment to complete (2-5 minutes)

### 4.5 Verify Deployment

1. Go to **Settings** > **Networking**
2. Under **Public Domain**, copy your Railway URL
3. Test endpoints:
   - Health: `https://[YOUR_URL].up.railway.app/health`
   - Docs: `https://[YOUR_URL].up.railway.app/docs`

**Expected Health Response:**
```json
{"status": "healthy", "service": "ORIONX"}
```

### 4.6 Copy Backend URL

Save your Railway backend URL - you'll need it for frontend:
```
https://[service-name].up.railway.app
```

---

## ⚡ STEP 5: DEPLOY FRONTEND TO VERCEL

### 5.1 Create Vercel Project

1. Go to **https://vercel.com**
2. Click **"Add New"** > **"Project"**
3. Import your GitHub repository
4. Select **ORIONX** repository

### 5.2 Configure Build Settings

1. **Framework Preset**: Next.js (auto-detected)
2. **Root Directory**: `frontend/`
3. **Build Command**: `npm run build` (default)
4. **Output Directory**: `.next` (default)
5. **Install Command**: `npm install` (default)

### 5.3 Add Environment Variables

Go to **Environment Variables** and add:

#### Variable 1: NEXT_PUBLIC_API_URL
- **Name**: `NEXT_PUBLIC_API_URL`
- **Value**: `https://[YOUR_RAILWAY_URL].up.railway.app` (from Step 4.6)
- **Environment**: Production, Preview, Development
- Click **"Add"**

#### Variable 2: NEXT_PUBLIC_SUPABASE_URL
- **Name**: `NEXT_PUBLIC_SUPABASE_URL`
- **Value**: `https://[PROJECT_REF].supabase.co` (from Step 1.3)
- **Environment**: Production, Preview, Development
- Click **"Add"**

#### Variable 3: NEXT_PUBLIC_SUPABASE_ANON_KEY
- **Name**: `NEXT_PUBLIC_SUPABASE_ANON_KEY`
- **Value**: `[YOUR_ANON_KEY]` (from Step 1.3)
- **Environment**: Production, Preview, Development
- Click **"Add"**

#### Variable 4: NEXT_PUBLIC_OPENROUTER_ENABLED
- **Name**: `NEXT_PUBLIC_OPENROUTER_ENABLED`
- **Value**: `true`
- **Environment**: Production, Preview, Development
- Click **"Add"**

### 5.4 Deploy

1. Click **"Deploy"**
2. Vercel will build and deploy automatically
3. Wait for deployment to complete (2-3 minutes)

### 5.5 Get Frontend URL

1. Once deployed, you'll see your Vercel URL
2. Format: `https://[project-name].vercel.app`
3. Copy this URL

### 5.6 Test Frontend

1. Visit your Vercel URL
2. Test:
   - Login/Register
   - API connectivity
   - WebSocket connections

---

## ✅ STEP 6: VERIFY COMPLETE DEPLOYMENT

### Backend Verification

```bash
# Health check
curl https://[YOUR_RAILWAY_URL].up.railway.app/health

# API docs
# Open in browser: https://[YOUR_RAILWAY_URL].up.railway.app/docs
```

### Frontend Verification

1. Visit your Vercel URL
2. Check browser console for errors
3. Test authentication
4. Test API calls
5. Test WebSocket connections

### Database Verification

1. Go to Supabase Dashboard > **Table Editor**
2. Verify all 9 tables exist
3. Test creating a user via frontend
4. Verify user appears in `users` table

### Redis Verification

1. Go to Upstash Dashboard
2. Go to **Console** tab
3. Run: `PING`
4. Should return: `PONG`

---

## 🔗 STEP 7: CONNECT ALL SERVICES

### Service Connections Verified:

- ✅ **Backend → Supabase**: Database connection via `SUPABASE_DB_URL`
- ✅ **Backend → Upstash Redis**: Cache connection via `REDIS_URL`
- ✅ **Frontend → Backend**: API calls via `NEXT_PUBLIC_API_URL`
- ✅ **Frontend → Supabase**: Direct client access via `NEXT_PUBLIC_SUPABASE_URL`
- ✅ **Frontend → OpenRouter**: AI features via `NEXT_PUBLIC_OPENROUTER_ENABLED`
- ✅ **Agents → Backend**: Task execution via backend API
- ✅ **WebSocket**: Real-time data via `wss://[RAILWAY_URL]/api/market/ws`

---

## 📝 EXACT PLACES TO PASTE KEYS

### Railway (Backend) - Variables Tab

1. Click on your service
2. Click **"Variables"** tab
3. Click **"New Variable"** button
4. Paste each variable:
   - `SUPABASE_DB_URL` → Paste connection string
   - `SUPABASE_SERVICE_ROLE_KEY` → Paste service role key
   - `REDIS_URL` → Paste Upstash Redis URL
   - `OPENROUTER_API_KEY` → Paste OpenRouter key
   - `SECRET_KEY` → Paste generated secret
   - `CORS_ORIGINS` → Type `*`

### Vercel (Frontend) - Environment Variables

1. Click on your project
2. Go to **Settings** tab
3. Click **"Environment Variables"** in sidebar
4. Click **"Add"** button
5. Paste each variable:
   - `NEXT_PUBLIC_API_URL` → Paste Railway URL
   - `NEXT_PUBLIC_SUPABASE_URL` → Paste Supabase URL
   - `NEXT_PUBLIC_SUPABASE_ANON_KEY` → Paste anon key
   - `NEXT_PUBLIC_OPENROUTER_ENABLED` → Type `true`

---

## 🎯 EXACT BUTTONS TO CLICK

### Railway

1. **"New Project"** → Top right
2. **"Deploy from GitHub repo"** → Select option
3. **"Settings"** tab → In service
4. **"Root Directory"** → Set to `backend`
5. **"Variables"** tab → Add environment variables
6. **"Deployments"** tab → Watch logs
7. **"Settings"** > **"Networking"** → Get public URL

### Vercel

1. **"Add New"** → Top right
2. **"Project"** → Select option
3. **"Import"** → Select repository
4. **"Settings"** tab → In project
5. **"Environment Variables"** → Add variables
6. **"Deploy"** button → Start deployment

---

## 🎉 DEPLOYMENT COMPLETE!

After completing all steps:

- ✅ Backend running on Railway
- ✅ Frontend running on Vercel
- ✅ Database on Supabase
- ✅ Redis on Upstash
- ✅ All services connected

**Your ORIONX application is now live in the cloud!** 🚀

---

## 📊 Final URLs Summary

After deployment, you should have:

- **Backend API**: `https://[service-name].up.railway.app`
- **Frontend App**: `https://[project-name].vercel.app`
- **API Docs**: `https://[service-name].up.railway.app/docs`
- **Health Check**: `https://[service-name].up.railway.app/health`
- **WebSocket**: `wss://[service-name].up.railway.app/api/market/ws`

---

## 🆘 Troubleshooting

See `RAILWAY_DEPLOYMENT_GUIDE.md` and `CLOUD_DEPLOYMENT_GUIDE.md` for detailed troubleshooting.

---

**Status**: ✅ **ALL SET — READY FOR PRODUCTION DEPLOY**

