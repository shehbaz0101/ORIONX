# 🎯 Railway Dashboard Deployment (No CLI Required)

## ✅ Fastest Method - Use Railway Web Dashboard

You can deploy completely via the Railway web interface - **no CLI login needed!**

---

## STEP 1: Create Railway Project

1. Go to **https://railway.app**
2. Click **"New Project"** (top right)
3. Select **"Deploy from GitHub repo"**
4. Authorize GitHub (if first time)
5. Select your **ORIONX** repository
6. Railway will automatically detect Python and start deploying

---

## STEP 2: Configure Service

1. Click on your service (the one that was created)
2. Go to **Settings** tab
3. **CRITICAL**: Under **Root Directory**, type: `backend`
4. Click **Save**

---

## STEP 3: Add Environment Variables

1. Still in your service, go to **Variables** tab
2. Click **"New Variable"** button
3. Add each variable below (one at a time):

### Variable 1:
- **Name**: `SUPABASE_DB_URL`
- **Value**: `postgresql+asyncpg://postgres:Pulsar%40220@db.fizlofuvxbdbbbqhjcgk.supabase.co:5432/postgres?sslmode=require`
- Click **Add**

### Variable 2:
- **Name**: `DATABASE_URL`
- **Value**: `postgresql+asyncpg://postgres:postgres@localhost:5432/orionx`
- Click **Add**

### Variable 3:
- **Name**: `REDIS_URL`
- **Value**: `redis://default:ATtxAAIncDI0NmFiZDJhMTA1ZGQ0ZWRhODBlZmI2ZmQ2Y2JkNTJjMXAyMTUyMTc@electric-walrus-15217.upstash.io:6379`
- Click **Add**

### Variable 4:
- **Name**: `UPSTASH_REDIS_URL`
- **Value**: `redis://localhost:6379/0`
- Click **Add**

### Variable 5:
- **Name**: `OPENROUTER_API_KEY`
- **Value**: `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`
- Click **Add**

### Variable 6:
- **Name**: `SECRET_KEY`
- **Value**: `aGohO5ZMAqH7Uel4Vr1LcyjznQW2siuRCFSIEfKTxtw`
- Click **Add**

### Variable 7:
- **Name**: `SUPABASE_SERVICE_ROLE_KEY`
- **Value**: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZpemxvZnV2eGJkYmJicWhqY2drIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2MzQ0MTYxMSwiZXhwIjoyMDc5MDE3NjExfQ.zE2ZnCP6xARgwc1htOZWiYyEvOtNP1kEo3csF_1s4s0`
- Click **Add**

### Variable 8:
- **Name**: `SUPABASE_PROJECT_URL`
- **Value**: `https://fizlofuvxbdbbbqhjcgk.supabase.co`
- Click **Add**

### Variable 9:
- **Name**: `SUPABASE_ANON_KEY`
- **Value**: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZpemxvZnV2eGJkYmJicWhqY2drIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjM0NDE2MTEsImV4cCI6MjA3OTAxNzYxMX0.1FKznPfZjVn-HQf3nIyuIIXCp0zcKiiNoNuENlcPxFc`
- Click **Add**

### Variable 10:
- **Name**: `CORS_ORIGINS`
- **Value**: `*`
- Click **Add**

### Variable 11:
- **Name**: `FRONTEND_DOMAIN`
- **Value**: `*`
- Click **Add**

---

## STEP 4: Verify Variables

After adding all 11 variables, you should see them listed in the Variables tab.

---

## STEP 5: Trigger Deployment

**Option A: Automatic (Recommended)**
- Push any commit to your GitHub repository
- Railway will automatically redeploy

**Option B: Manual**
1. Go to **Deployments** tab
2. Click **"Redeploy"** button
3. Watch the build logs

---

## STEP 6: Monitor Deployment

1. Go to **Deployments** tab
2. Click on the latest deployment
3. Watch logs for:
   - ✅ `Successfully installed` (dependencies)
   - ✅ `Starting ORIONX backend...`
   - ✅ `ORIONX backend started successfully`
   - ✅ `Application startup complete`

---

## STEP 7: Get Backend URL

1. Go to **Settings** tab
2. Scroll to **Networking** section
3. Under **Public Domain**, you'll see your Railway URL
4. Format: `https://[service-name].up.railway.app`
5. **Copy this URL** - you'll need it for frontend

---

## STEP 8: Test Backend

Open in browser or use curl:
```
https://[YOUR_RAILWAY_URL].up.railway.app/health
```

**Expected response:**
```json
{"status": "healthy", "service": "ORIONX"}
```

**API Docs:**
```
https://[YOUR_RAILWAY_URL].up.railway.app/docs
```

---

## ✅ That's It!

**No CLI, no login, no scripts needed!**

Everything can be done via the Railway web dashboard.

---

## Next: Deploy Frontend

After backend is working:
1. Update `frontend/.env.production` with your Railway URL
2. Deploy to Vercel (also via dashboard - no CLI needed)

---

**Start now:** Go to https://railway.app and create a new project!

