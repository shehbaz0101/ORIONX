# ⚡ ORIONX Quick Deployment Guide

## 🎯 Fastest Path to Deploy

### 1️⃣ Install Railway CLI
```bash
npm install -g @railway/cli
```

### 2️⃣ Login
```bash
railway login
```

### 3️⃣ Create Project (Dashboard)
- Go to https://railway.app
- New Project → Deploy from GitHub
- Select ORIONX repo
- **Set Root Directory to: `backend`**

### 4️⃣ Push Variables
```powershell
.\railway-deploy.ps1
```
Enter your service name when prompted.

### 5️⃣ Deploy
- Push to GitHub, OR
- Railway Dashboard → Redeploy

### 6️⃣ Get URL
- Settings → Networking → Public Domain
- Copy: `https://[name].up.railway.app`

### 7️⃣ Test
```bash
curl https://[YOUR_URL].up.railway.app/health
```

### 8️⃣ Deploy Frontend
- Update `frontend/.env.production` with Railway URL
- Deploy to Vercel (see `VERCEL_DEPLOYMENT_STEPS.md`)

---

**That's it!** 🎉

