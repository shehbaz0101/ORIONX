# 🚀 ORIONX Railway Deployment - Step-by-Step Guide

## Prerequisites

- ✅ Railway account created
- ✅ GitHub repository connected
- ✅ Railway CLI installed (`npm install -g @railway/cli`)

---

## Step 1: Install Railway CLI (if not installed)

```bash
npm install -g @railway/cli
```

---

## Step 2: Login to Railway

```bash
railway login
```

This will open your browser to authenticate.

---

## Step 3: Create Railway Project

### Option A: Via Railway Dashboard
1. Go to https://railway.app
2. Click **"New Project"**
3. Select **"Deploy from GitHub repo"**
4. Choose your **ORIONX** repository
5. Railway will auto-detect it's a Python project

### Option B: Via Railway CLI
```bash
railway init
# Select: Deploy from GitHub repo
# Choose: ORIONX repository
```

---

## Step 4: Configure Service Settings

1. In Railway Dashboard, click on your service
2. Go to **Settings** tab
3. **IMPORTANT**: Set **Root Directory** to: `backend`
4. Click **Save**

---

## Step 5: Push Environment Variables

### Run the deployment script:

```powershell
.\railway-deploy.ps1
```

The script will:
- Check Railway CLI installation
- Verify login status
- Ask for your service name
- Push all 12 environment variables automatically

### Or manually via Railway CLI:

```bash
railway variables set SUPABASE_DB_URL="postgresql+asyncpg://postgres:Pulsar%40220@db.fizlofuvxbdbbbqhjcgk.supabase.co:5432/postgres?sslmode=require" --service [YOUR_SERVICE_NAME]
railway variables set DATABASE_URL="postgresql+asyncpg://postgres:postgres@localhost:5432/orionx" --service [YOUR_SERVICE_NAME]
railway variables set REDIS_URL="redis://default:ATtxAAIncDI0NmFiZDJhMTA1ZGQ0ZWRhODBlZmI2ZmQ2Y2JkNTJjMXAyMTUyMTc@electric-walrus-15217.upstash.io:6379" --service [YOUR_SERVICE_NAME]
railway variables set UPSTASH_REDIS_URL="redis://localhost:6379/0" --service [YOUR_SERVICE_NAME]
railway variables set OPENROUTER_API_KEY="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" --service [YOUR_SERVICE_NAME]
railway variables set SECRET_KEY="aGohO5ZMAqH7Uel4Vr1LcyjznQW2siuRCFSIEfKTxtw" --service [YOUR_SERVICE_NAME]
railway variables set SUPABASE_SERVICE_ROLE_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZpemxvZnV2eGJkYmJicWhqY2drIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2MzQ0MTYxMSwiZXhwIjoyMDc5MDE3NjExfQ.zE2ZnCP6xARgwc1htOZWiYyEvOtNP1kEo3csF_1s4s0" --service [YOUR_SERVICE_NAME]
railway variables set SUPABASE_PROJECT_URL="https://fizlofuvxbdbbbqhjcgk.supabase.co" --service [YOUR_SERVICE_NAME]
railway variables set SUPABASE_ANON_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZpemxvZnV2eGJkYmJicWhqY2drIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjM0NDE2MTEsImV4cCI6MjA3OTAxNzYxMX0.1FKznPfZjVn-HQf3nIyuIIXCp0zcKiiNoNuENlcPxFc" --service [YOUR_SERVICE_NAME]
railway variables set CORS_ORIGINS="*" --service [YOUR_SERVICE_NAME]
railway variables set FRONTEND_DOMAIN="*" --service [YOUR_SERVICE_NAME]
```

---

## Step 6: Verify Variables in Railway Dashboard

1. Go to Railway Dashboard
2. Click on your service
3. Go to **Variables** tab
4. Verify all 12 variables are present

---

## Step 7: Trigger Deployment

### Option A: Automatic (GitHub Push)
- Push any commit to your GitHub repository
- Railway will automatically deploy

### Option B: Manual Trigger
1. Go to Railway Dashboard
2. Click on your service
3. Go to **Deployments** tab
4. Click **"Redeploy"**

---

## Step 8: Monitor Build Logs

1. In **Deployments** tab, click on the latest deployment
2. Watch for:
   - ✅ `Successfully installed` messages
   - ✅ `Starting ORIONX backend...`
   - ✅ `ORIONX backend started successfully`
   - ✅ `Application startup complete`

---

## Step 9: Get Backend URL

1. Go to **Settings** > **Networking**
2. Under **Public Domain**, copy your Railway URL
3. Format: `https://[service-name].up.railway.app`
4. **Save this URL** - you'll need it for frontend deployment

---

## Step 10: Test Backend

```bash
# Health check
curl https://[YOUR_RAILWAY_URL].up.railway.app/health

# API docs
# Open in browser: https://[YOUR_RAILWAY_URL].up.railway.app/docs
```

Expected health response:
```json
{"status": "healthy", "service": "ORIONX"}
```

---

## Next: Frontend Deployment

After backend is deployed and tested, proceed to Vercel deployment.

