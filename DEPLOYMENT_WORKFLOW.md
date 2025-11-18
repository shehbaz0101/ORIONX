# 🚀 ORIONX Complete Deployment Workflow

## Prerequisites Check

- [x] Railway CLI installed (`npm install -g @railway/cli`)
- [ ] Railway account created
- [ ] Logged in to Railway (`railway login`)
- [ ] Railway project created for ORIONX
- [ ] Root directory set to `backend` in Railway

---

## STEP 1: Login to Railway (Required)

**Run this command:**
```bash
railway login
```

This will open your browser. Complete the login, then continue.

---

## STEP 2: Create Railway Project (If Not Done)

1. Go to https://railway.app
2. Click **"New Project"**
3. Select **"Deploy from GitHub repo"**
4. Authorize GitHub (if needed)
5. Select **ORIONX** repository
6. **CRITICAL**: Go to Settings → Set **Root Directory** to: `backend`

---

## STEP 3: Run Automated Deployment

**After logging in and creating project, run:**

```powershell
.\FULL_AUTO_DEPLOY.ps1
```

**Or with service name:**
```powershell
.\FULL_AUTO_DEPLOY.ps1 -RailwayServiceName "your-service-name"
```

---

## What Happens Next

The script will:
1. Push all 12 environment variables to Railway
2. Trigger backend deployment
3. Wait for deployment
4. Get Railway backend URL
5. Test backend health endpoint
6. Update frontend env with Railway URL
7. Deploy frontend to Vercel
8. Test all endpoints
9. Output final URLs

---

## Manual Alternative

If automation fails, use:
- `railway-deploy.ps1` - Just pushes variables
- `RAILWAY_DEPLOYMENT_STEPS.md` - Manual Railway steps
- `VERCEL_DEPLOYMENT_STEPS.md` - Manual Vercel steps

---

## Expected Final Output

```
BACKEND_URL: https://[service-name].up.railway.app
FRONTEND_URL: https://[project-name].vercel.app
STATUS: FULLY DEPLOYED AND VERIFIED
```

---

**Start with:** `railway login`

