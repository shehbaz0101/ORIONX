# 🚀 Show Me The App - Quick Deployment

## ⚡ Fastest Path to See ORIONX Live

I've prepared everything. Here's the **5-minute deployment** process:

---

## 🎯 STEP 1: Deploy Backend to Railway (3 min)

### Quick Steps:

1. **Open:** https://railway.app
2. **Click:** "New Project" → "Deploy from GitHub repo"
3. **Select:** `shehbaz0101/ORIONX`
4. **Settings:** Set Root Directory to `backend`
5. **Variables:** Add 11 variables (see below)
6. **Get URL:** Settings → Networking → Public Domain

### Environment Variables (Copy-Paste):

Open `ENV_VARIABLES_QUICK_COPY.md` and copy all 11 variables, or use this quick list:

```
SUPABASE_DB_URL=postgresql+asyncpg://postgres:Pulsar%40220@db.fizlofuvxbdbbbqhjcgk.supabase.co:5432/postgres?sslmode=require
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/orionx
REDIS_URL=redis://default:ATtxAAIncDI0NmFiZDJhMTA1ZGQ0ZWRhODBlZmI2ZmQ2Y2JkNTJjMXAyMTUyMTc@electric-walrus-15217.upstash.io:6379
UPSTASH_REDIS_URL=redis://localhost:6379/0
OPENROUTER_API_KEY=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
SECRET_KEY=aGohO5ZMAqH7Uel4Vr1LcyjznQW2siuRCFSIEfKTxtw
SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZpemxvZnV2eGJkYmJicWhqY2drIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2MzQ0MTYxMSwiZXhwIjoyMDc5MDE3NjExfQ.zE2ZnCP6xARgwc1htOZWiYyEvOtNP1kEo3csF_1s4s0
SUPABASE_PROJECT_URL=https://fizlofuvxbdbbbqhjcgk.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZpemxvZnV2eGJkYmJicWhqY2drIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjM0NDE2MTEsImV4cCI6MjA3OTAxNzYxMX0.1FKznPfZjVn-HQf3nIyuIIXCp0zcKiiNoNuENlcPxFc
CORS_ORIGINS=*
FRONTEND_DOMAIN=*
```

**Save your Railway URL!** You'll need it for frontend.

---

## 🎯 STEP 2: Deploy Frontend to Vercel (2 min)

### Quick Steps:

1. **Open:** https://vercel.com
2. **Click:** "Add New" → "Project"
3. **Import:** `shehbaz0101/ORIONX`
4. **Settings:**
   - Root Directory: `frontend`
   - Framework: Next.js (auto)
5. **Environment Variables:** Add 4 variables (see below)
6. **Deploy:** Click "Deploy"

### Environment Variables (Replace [RAILWAY_URL] with your Railway URL):

```
NEXT_PUBLIC_API_URL=https://[YOUR_RAILWAY_URL].up.railway.app
NEXT_PUBLIC_SUPABASE_URL=https://fizlofuvxbdbbbqhjcgk.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZpemxvZnV2eGJkYmJicWhqY2drIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjM0NDE2MTEsImV4cCI6MjA3OTAxNzYxMX0.1FKznPfZjVn-HQf3nIyuIIXCp0zcKiiNoNuENlcPxFc
NEXT_PUBLIC_OPENROUTER_ENABLED=true
```

---

## ✅ STEP 3: Verify & Show App

After both deployments complete:

1. **Get your URLs:**
   - Railway Backend: `https://[name].up.railway.app`
   - Vercel Frontend: `https://[name].vercel.app`

2. **Test Backend:**
   ```
   https://[RAILWAY_URL]/health
   ```
   Should show: `{"status": "healthy", "service": "ORIONX"}`

3. **Test Frontend:**
   ```
   https://[VERCEL_URL]
   ```
   Should show: ORIONX dashboard

4. **Run Verification Script:**
   ```powershell
   .\verify-deployment.ps1 -RailwayUrl "https://[YOUR_RAILWAY_URL]" -VercelUrl "https://[YOUR_VERCEL_URL]"
   ```

---

## 🎉 Your App is Live!

**Open your frontend URL in browser to see ORIONX!**

---

## 📋 Quick Checklist

- [ ] Railway project created
- [ ] Root directory set to `backend`
- [ ] 11 environment variables added
- [ ] Railway URL obtained
- [ ] Vercel project created
- [ ] Root directory set to `frontend`
- [ ] 4 environment variables added (with Railway URL)
- [ ] Vercel deployment complete
- [ ] Frontend URL obtained
- [ ] App tested and working

---

**Start now:** https://railway.app → New Project

