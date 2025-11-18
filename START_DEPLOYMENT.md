# 🚀 ORIONX Full Deployment - Start Here

## ✅ Preparation Complete

All environment files and deployment scripts are ready:
- ✅ `backend/.env.production` - Created with all credentials
- ✅ `frontend/.env.production` - Created (Railway URL placeholder)
- ✅ `railway-deploy.ps1` - Automated deployment script
- ✅ Deployment guides created

---

## 📋 Step-by-Step Deployment Process

### PHASE 1: Install Railway CLI

**Option 1: Via npm (Recommended)**
```bash
npm install -g @railway/cli
```

**Option 2: Via Direct Download**
- Go to https://railway.app/cli
- Download for Windows
- Add to PATH

**Verify Installation:**
```bash
railway --version
```

---

### PHASE 2: Login to Railway

```bash
railway login
```

This will open your browser to authenticate with Railway.

---

### PHASE 3: Create Railway Project

**Option A: Via Railway Dashboard (Easier)**
1. Go to https://railway.app
2. Click **"New Project"**
3. Select **"Deploy from GitHub repo"**
4. Authorize GitHub (if needed)
5. Select **ORIONX** repository
6. Railway will auto-detect Python

**Option B: Via Railway CLI**
```bash
railway init
# Follow prompts to connect GitHub repo
```

---

### PHASE 4: Configure Service

1. In Railway Dashboard, click on your service
2. Go to **Settings** tab
3. **CRITICAL**: Set **Root Directory** to: `backend`
4. Click **Save**

---

### PHASE 5: Push Environment Variables

**Run the automated script:**
```powershell
.\railway-deploy.ps1
```

The script will:
- Check Railway CLI
- Verify login
- Ask for your service name
- Push all 12 environment variables

**Or manually via CLI:**
See `RAILWAY_DEPLOYMENT_STEPS.md` for individual commands.

---

### PHASE 6: Trigger Deployment

**Option A: Automatic (Recommended)**
- Push any commit to GitHub
- Railway auto-deploys

**Option B: Manual**
- Railway Dashboard > Deployments > Redeploy

---

### PHASE 7: Monitor Build

1. Go to **Deployments** tab
2. Click latest deployment
3. Watch logs for:
   - ✅ `Successfully installed`
   - ✅ `Starting ORIONX backend...`
   - ✅ `ORIONX backend started successfully`

---

### PHASE 8: Get Backend URL

1. **Settings** > **Networking** > **Public Domain**
2. Copy URL: `https://[service-name].up.railway.app`
3. **SAVE THIS URL** - needed for frontend

---

### PHASE 9: Test Backend

```bash
# Health check
curl https://[YOUR_RAILWAY_URL].up.railway.app/health

# Should return: {"status": "healthy", "service": "ORIONX"}
```

**API Docs:**
Open: `https://[YOUR_RAILWAY_URL].up.railway.app/docs`

---

### PHASE 10: Deploy Frontend to Vercel

After backend is working:

1. **Update frontend/.env.production** with Railway URL
2. Follow `VERCEL_DEPLOYMENT_STEPS.md`
3. Deploy to Vercel
4. Test frontend → backend connection

---

## 🎯 Quick Start Commands

```bash
# 1. Install Railway CLI
npm install -g @railway/cli

# 2. Login
railway login

# 3. Create project (via dashboard is easier)
# Go to railway.app > New Project > Deploy from GitHub

# 4. Push variables
.\railway-deploy.ps1

# 5. Deploy (push to GitHub or click Redeploy)
```

---

## 📞 Need Help?

- Railway Docs: https://docs.railway.app
- Railway CLI: https://railway.app/cli
- See `RAILWAY_DEPLOYMENT_STEPS.md` for detailed steps

---

**Ready to start?** Begin with Phase 1: Install Railway CLI

