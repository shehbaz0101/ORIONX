# 🚀 DEPLOY ORIONX NOW

## Quick Start

### Step 1: Login to Railway (One-time)

```bash
railway login
```

This opens your browser - complete the login.

### Step 2: Create Railway Project (if not done)

1. Go to https://railway.app
2. Click **"New Project"**
3. Select **"Deploy from GitHub repo"**
4. Choose **ORIONX** repository
5. **IMPORTANT**: In Settings, set **Root Directory** to: `backend`

### Step 3: Run Full Auto-Deploy

```powershell
.\FULL_AUTO_DEPLOY.ps1
```

When prompted, enter your Railway service name.

---

## What the Script Does

1. ✅ Pushes all 12 environment variables to Railway
2. ✅ Triggers Railway deployment
3. ✅ Gets Railway backend URL
4. ✅ Tests backend health endpoint
5. ✅ Updates frontend/.env.production with Railway URL
6. ✅ Deploys frontend to Vercel
7. ✅ Tests all endpoints
8. ✅ Outputs final URLs

---

## Alternative: Manual Steps

If automation doesn't work, see:
- `RAILWAY_DEPLOYMENT_STEPS.md` - Railway manual steps
- `VERCEL_DEPLOYMENT_STEPS.md` - Vercel manual steps

---

## Expected Output

After running the script, you'll get:

```
BACKEND_URL: https://[service-name].up.railway.app
FRONTEND_URL: https://[project-name].vercel.app
STATUS: FULLY DEPLOYED
```

---

**Ready?** Run: `.\FULL_AUTO_DEPLOY.ps1`

