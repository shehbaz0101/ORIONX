# 🚀 DEPLOY ORIONX NOW - Fastest Method

## ⚡ 5-Minute Deployment Guide

### STEP 1: Railway Backend (3 minutes)

1. **Go to Railway Dashboard:**
   - https://railway.app
   - Login or create account

2. **Create Project:**
   - Click **"New Project"** (top right)
   - Select **"Deploy from GitHub repo"**
   - Authorize GitHub (if needed)
   - Select repository: **shehbaz0101/ORIONX**
   - Railway will auto-detect and start deploying

3. **Configure Service:**
   - Click on your service
   - Go to **Settings** tab
   - Find **"Root Directory"**
   - Set to: `backend`
   - Click **Save**

4. **Add Environment Variables:**
   - Go to **Variables** tab
   - Click **"New Variable"** 11 times
   - Copy-paste from `ENV_VARIABLES_QUICK_COPY.md`:

**Quick Copy List:**
```
SUPABASE_DB_URL = postgresql+asyncpg://postgres:Pulsar%40220@db.fizlofuvxbdbbbqhjcgk.supabase.co:5432/postgres?sslmode=require
DATABASE_URL = postgresql+asyncpg://postgres:postgres@localhost:5432/orionx
REDIS_URL = redis://default:ATtxAAIncDI0NmFiZDJhMTA1ZGQ0ZWRhODBlZmI2ZmQ2Y2JkNTJjMXAyMTUyMTc@electric-walrus-15217.upstash.io:6379
UPSTASH_REDIS_URL = redis://localhost:6379/0
OPENROUTER_API_KEY = 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
SECRET_KEY = aGohO5ZMAqH7Uel4Vr1LcyjznQW2siuRCFSIEfKTxtw
SUPABASE_SERVICE_ROLE_KEY = eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZpemxvZnV2eGJkYmJicWhqY2drIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2MzQ0MTYxMSwiZXhwIjoyMDc5MDE3NjExfQ.zE2ZnCP6xARgwc1htOZWiYyEvOtNP1kEo3csF_1s4s0
SUPABASE_PROJECT_URL = https://fizlofuvxbdbbbqhjcgk.supabase.co
SUPABASE_ANON_KEY = eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZpemxvZnV2eGJkYmJicWhqY2drIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjM0NDE2MTEsImV4cCI6MjA3OTAxNzYxMX0.1FKznPfZjVn-HQf3nIyuIIXCp0zcKiiNoNuENlcPxFc
CORS_ORIGINS = *
FRONTEND_DOMAIN = *
```

5. **Get Backend URL:**
   - Go to **Settings** → **Networking**
   - Under **"Public Domain"**, copy your URL
   - Format: `https://[name].up.railway.app`
   - **SAVE THIS URL** - you'll need it for frontend

6. **Test Backend:**
   - Open: `https://[YOUR_URL].up.railway.app/health`
   - Should show: `{"status": "healthy", "service": "ORIONX"}`

---

### STEP 2: Vercel Frontend (2 minutes)

1. **Go to Vercel Dashboard:**
   - https://vercel.com
   - Login or create account

2. **Create Project:**
   - Click **"Add New"** → **"Project"**
   - Import Git Repository
   - Select **shehbaz0101/ORIONX**

3. **Configure Project:**
   - **Framework Preset:** Next.js (auto-detected)
   - **Root Directory:** `frontend`
   - **Build Command:** `npm run build` (default)
   - **Output Directory:** `.next` (default)

4. **Add Environment Variables:**
   - Go to **Environment Variables** section
   - Add these 4 variables:

```
NEXT_PUBLIC_API_URL = https://[YOUR_RAILWAY_URL].up.railway.app
NEXT_PUBLIC_SUPABASE_URL = https://fizlofuvxbdbbbqhjcgk.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY = eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZpemxvZnV2eGJkYmJicWhqY2drIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjM0NDE2MTEsImV4cCI6MjA3OTAxNzYxMX0.1FKznPfZjVn-HQf3nIyuIIXCp0zcKiiNoNuENlcPxFc
NEXT_PUBLIC_OPENROUTER_ENABLED = true
```

   - Replace `[YOUR_RAILWAY_URL]` with your actual Railway URL

5. **Deploy:**
   - Click **"Deploy"**
   - Wait 2-3 minutes for build

6. **Get Frontend URL:**
   - Once deployed, you'll see your Vercel URL
   - Format: `https://[project-name].vercel.app`

---

## ✅ That's It!

**Your ORIONX app is now live!**

- **Backend:** `https://[name].up.railway.app`
- **Frontend:** `https://[name].vercel.app`

---

## 🧪 Test Your Deployment

1. **Backend Health:**
   ```
   https://[RAILWAY_URL]/health
   ```

2. **Backend API Docs:**
   ```
   https://[RAILWAY_URL]/docs
   ```

3. **Frontend App:**
   ```
   https://[VERCEL_URL]
   ```

---

**Start now:** Go to https://railway.app and create your project!

