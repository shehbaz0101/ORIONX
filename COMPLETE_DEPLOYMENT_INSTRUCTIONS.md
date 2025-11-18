# 🚀 ORIONX Complete Deployment Instructions

## ⚠️ IMPORTANT: Start Here

Railway login requires interactive browser authentication, so you need to login first.

---

## STEP 1: Login to Railway (Required)

**Run this command in your terminal:**
```bash
railway login
```

A browser window will open. Complete the login, then return here.

**Verify login:**
```bash
railway whoami
```

You should see your email address.

---

## STEP 2: Create Railway Project (If Not Done)

1. Go to https://railway.app
2. Click **"New Project"** (top right)
3. Select **"Deploy from GitHub repo"**
4. Authorize GitHub (if first time)
5. Select your **ORIONX** repository
6. **CRITICAL**: 
   - Click on the service
   - Go to **Settings** tab
   - Set **Root Directory** to: `backend`
   - Click **Save**

---

## STEP 3: Run Automated Deployment

**After login and project creation, run:**

```powershell
.\deploy-after-login.ps1 -ServiceName "your-service-name"
```

**Replace `your-service-name` with your actual Railway service name.**

The script will:
1. ✅ Push all 12 environment variables
2. ✅ Trigger deployment
3. ✅ Get backend URL
4. ✅ Test health endpoint
5. ✅ Save URL to file

---

## STEP 4: Get Your Service Name

If you don't know your service name:
1. Go to Railway Dashboard
2. Look at your project
3. The service name is shown under the service card
4. Or run: `railway status` (if linked)

---

## STEP 5: After Backend Deploys

Once you have the backend URL:

1. **Update frontend env:**
   ```powershell
   # The backend URL will be in RAILWAY_BACKEND_URL.txt
   $backendUrl = Get-Content RAILWAY_BACKEND_URL.txt
   $content = @"
   NEXT_PUBLIC_API_URL=$backendUrl
   NEXT_PUBLIC_SUPABASE_URL=https://fizlofuvxbdbbbqhjcgk.supabase.co
   NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZpemxvZnV2eGJkYmJicWhqY2drIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjM0NDE2MTEsImV4cCI6MjA3OTAxNzYxMX0.1FKznPfZjVn-HQf3nIyuIIXCp0zcKiiNoNuENlcPxFc
   NEXT_PUBLIC_OPENROUTER_ENABLED=true
   "@
   $content | Out-File -FilePath "frontend\.env.production" -Encoding utf8
   ```

2. **Deploy to Vercel:**
   - Go to https://vercel.com
   - Add New > Project
   - Import ORIONX repository
   - Set Root Directory: `frontend`
   - Add environment variables from `frontend/.env.production`
   - Deploy

---

## Alternative: Manual Variable Push

If the script doesn't work, push variables manually:

```bash
railway variables set SUPABASE_DB_URL="postgresql+asyncpg://postgres:Pulsar%40220@db.fizlofuvxbdbbbqhjcgk.supabase.co:5432/postgres?sslmode=require" --service YOUR_SERVICE_NAME
railway variables set REDIS_URL="redis://default:ATtxAAIncDI0NmFiZDJhMTA1ZGQ0ZWRhODBlZmI2ZmQ2Y2JkNTJjMXAyMTUyMTc@electric-walrus-15217.upstash.io:6379" --service YOUR_SERVICE_NAME
railway variables set OPENROUTER_API_KEY="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" --service YOUR_SERVICE_NAME
railway variables set SECRET_KEY="aGohO5ZMAqH7Uel4Vr1LcyjznQW2siuRCFSIEfKTxtw" --service YOUR_SERVICE_NAME
railway variables set SUPABASE_SERVICE_ROLE_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZpemxvZnV2eGJkYmJicWhqY2drIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2MzQ0MTYxMSwiZXhwIjoyMDc5MDE3NjExfQ.zE2ZnCP6xARgwc1htOZWiYyEvOtNP1kEo3csF_1s4s0" --service YOUR_SERVICE_NAME
railway variables set SUPABASE_PROJECT_URL="https://fizlofuvxbdbbbqhjcgk.supabase.co" --service YOUR_SERVICE_NAME
railway variables set SUPABASE_ANON_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZpemxvZnV2eGJkYmJicWhqY2drIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjM0NDE2MTEsImV4cCI6MjA3OTAxNzYxMX0.1FKznPfZjVn-HQf3nIyuIIXCp0zcKiiNoNuENlcPxFc" --service YOUR_SERVICE_NAME
railway variables set CORS_ORIGINS="*" --service YOUR_SERVICE_NAME
railway variables set FRONTEND_DOMAIN="*" --service YOUR_SERVICE_NAME
```

---

## Quick Start Commands

```bash
# 1. Login
railway login

# 2. Run deployment (replace SERVICE_NAME)
.\deploy-after-login.ps1 -ServiceName "SERVICE_NAME"

# 3. Check deployment
railway logs --service SERVICE_NAME

# 4. Get URL
railway domain --service SERVICE_NAME
```

---

**Start with:** `railway login`

