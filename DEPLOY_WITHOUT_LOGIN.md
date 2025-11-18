# 🚀 Deploy ORIONX Without Railway CLI Login

Yes! There are several ways to deploy without interactive login:

---

## Option 1: Railway Dashboard (Easiest - No CLI Needed)

### Step 1: Create Project via Dashboard
1. Go to https://railway.app
2. Click **"New Project"**
3. Select **"Deploy from GitHub repo"**
4. Choose **ORIONX** repository
5. Railway auto-detects Python and starts deploying

### Step 2: Set Root Directory
1. Click on your service
2. Go to **Settings** tab
3. Set **Root Directory** to: `backend`
4. Click **Save**

### Step 3: Add Environment Variables (Dashboard UI)
1. Go to **Variables** tab
2. Click **"New Variable"** for each:

**Copy and paste these one by one:**

```
SUPABASE_DB_URL=postgresql+asyncpg://postgres:Pulsar%40220@db.fizlofuvxbdbbbqhjcgk.supabase.co:5432/postgres?sslmode=require
```

```
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/orionx
```

```
REDIS_URL=redis://default:ATtxAAIncDI0NmFiZDJhMTA1ZGQ0ZWRhODBlZmI2ZmQ2Y2JkNTJjMXAyMTUyMTc@electric-walrus-15217.upstash.io:6379
```

```
UPSTASH_REDIS_URL=redis://localhost:6379/0
```

```
OPENROUTER_API_KEY=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
```

```
SECRET_KEY=aGohO5ZMAqH7Uel4Vr1LcyjznQW2siuRCFSIEfKTxtw
```

```
SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZpemxvZnV2eGJkYmJicWhqY2drIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2MzQ0MTYxMSwiZXhwIjoyMDc5MDE3NjExfQ.zE2ZnCP6xARgwc1htOZWiYyEvOtNP1kEo3csF_1s4s0
```

```
SUPABASE_PROJECT_URL=https://fizlofuvxbdbbbqhjcgk.supabase.co
```

```
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZpemxvZnV2eGJkYmJicWhqY2drIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjM0NDE2MTEsImV4cCI6MjA3OTAxNzYxMX0.1FKznPfZjVn-HQf3nIyuIIXCp0zcKiiNoNuENlcPxFc
```

```
CORS_ORIGINS=*
```

```
FRONTEND_DOMAIN=*
```

### Step 4: Deploy
- Railway auto-deploys when you push to GitHub
- Or click **"Redeploy"** in Deployments tab

### Step 5: Get Backend URL
1. Go to **Settings** > **Networking**
2. Under **Public Domain**, copy your URL
3. Format: `https://[service-name].up.railway.app`

---

## Option 2: Railway API Token (Programmatic)

### Get API Token
1. Go to Railway Dashboard
2. Click your profile (top right)
3. Go to **Settings** > **Tokens**
4. Click **"New Token"**
5. Copy the token

### Use API Script
```powershell
.\railway-api-deploy.ps1 -RailwayApiToken "YOUR_TOKEN" -ProjectId "YOUR_PROJECT_ID" -ServiceId "YOUR_SERVICE_ID"
```

**To get Project ID and Service ID:**
- Project ID: Railway Dashboard URL or project settings
- Service ID: Service settings page URL

---

## Option 3: GitHub Actions (Fully Automated)

### Setup
1. Go to Railway Dashboard
2. Get your **Railway Token** (Settings > Tokens)
3. Go to GitHub > Your Repo > Settings > Secrets
4. Add secret: `RAILWAY_TOKEN` = your Railway token
5. Add secret: `RAILWAY_PROJECT_ID` = your project ID

### Deploy
- Push to `main` branch
- GitHub Actions will auto-deploy
- See `.github/workflows/deploy-railway.yml`

---

## Option 4: Railway CLI with Token (Non-Interactive)

```bash
# Set token as environment variable
export RAILWAY_TOKEN=your_token_here

# Then use CLI commands
railway variables set KEY=value --service SERVICE_NAME
```

---

## 🎯 Recommended: Dashboard Method

**Easiest and fastest:**
1. Use Railway Dashboard UI
2. Add variables manually (copy-paste from above)
3. Railway auto-deploys on git push

**No CLI, no login, no scripts needed!**

---

## After Backend Deploys

1. Get Railway backend URL
2. Update `frontend/.env.production` with Railway URL
3. Deploy frontend to Vercel (also via dashboard - no CLI needed)

---

**Choose the method that works best for you!**

