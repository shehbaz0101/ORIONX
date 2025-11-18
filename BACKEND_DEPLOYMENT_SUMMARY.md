# ORIONX Backend - Railway Deployment Summary

## ✅ Backend Preparation Complete

### 1. Configuration Files Created/Updated

- ✅ **Procfile**: `web: uvicorn main:app --host 0.0.0.0 --port $PORT`
- ✅ **railway.json**: Railway service configuration
- ✅ **runtime.txt**: Python 3.11 specification
- ✅ **.python-version**: Python 3.11 specification
- ✅ **requirements.txt**: All dependencies listed

### 2. Environment Variables Configured

The backend is configured to use:
- `SUPABASE_DB_URL` - Supabase database connection (with fallback to `DATABASE_URL`)
- `UPSTASH_REDIS_URL` - Upstash Redis connection (with fallback to `REDIS_URL`)
- `OPENROUTER_API_KEY` - AI API key
- `SECRET_KEY` - JWT secret key
- `FRONTEND_DOMAIN` - Optional, for CORS
- `VERCEL_URL` - Optional, auto-set by Vercel
- `PORT` - Automatically provided by Railway

### 3. Code Validation

- ✅ All FastAPI imports use `backend.` prefix (compatible with Railway root directory)
- ✅ No hardcoded localhost URLs (all use environment variables)
- ✅ WebSocket support configured for Railway
- ✅ CORS configured for Vercel domains
- ✅ Database connection uses Supabase URL
- ✅ Redis connection uses Upstash URL

### 4. Deployment Artifacts

All necessary files are in the `backend/` directory:
- `main.py` - FastAPI application
- `api.py` - Router aggregation
- `Procfile` - Railway process file
- `railway.json` - Service configuration
- `requirements.txt` - Dependencies
- `runtime.txt` - Python version
- `.python-version` - Python version
- All source code modules

---

## 🚀 Railway Deployment Instructions

### Step 1: Create Railway Project

1. Go to https://railway.app
2. Click **"New Project"**
3. Select **"Deploy from GitHub repo"**
4. Authorize GitHub (if needed)
5. Select **ORIONX** repository

### Step 2: Configure Service

1. Click on the service
2. Go to **Settings** tab
3. Set **Root Directory** to: `backend`
4. Click **Save**

### Step 3: Add Environment Variables

Go to **Variables** tab and add:

```bash
SUPABASE_DB_URL=postgresql+asyncpg://postgres:[PASSWORD]@db.[PROJECT_REF].supabase.co:5432/postgres
UPSTASH_REDIS_URL=redis://default:[PASSWORD]@[ENDPOINT].upstash.io:[PORT]
OPENROUTER_API_KEY=sk-or-v1-[YOUR_KEY]
SECRET_KEY=[GENERATE_32_CHAR_RANDOM_STRING]
```

**Generate SECRET_KEY:**
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### Step 4: Deploy

1. Railway will auto-deploy on git push
2. Or click **"Redeploy"** in Deployments tab
3. Watch logs in **Deployments** tab

### Step 5: Verify Deployment

1. Get your Railway URL from **Settings** > **Networking** > **Public Domain**
2. Test endpoints:
   - Health: `https://[URL].up.railway.app/health`
   - Docs: `https://[URL].up.railway.app/docs`
   - Root: `https://[URL].up.railway.app/`

---

## 📋 Expected Output After Deployment

### Service Information

- **Service Name**: `orionx-backend` (or custom name)
- **Public API URL**: `https://[service-name].up.railway.app`
- **Health Check**: `https://[service-name].up.railway.app/health`
- **API Documentation**: `https://[service-name].up.railway.app/docs`
- **WebSocket URL**: `wss://[service-name].up.railway.app/api/market/ws`

### Verification Commands

```bash
# Health check
curl https://[YOUR_RAILWAY_URL].up.railway.app/health

# Expected: {"status": "healthy", "service": "ORIONX"}

# API docs (open in browser)
https://[YOUR_RAILWAY_URL].up.railway.app/docs
```

---

## 🔍 Deployment Checklist

Before deploying:
- [ ] Railway account created
- [ ] GitHub repository connected
- [ ] Root directory set to `backend`
- [ ] All environment variables added
- [ ] SECRET_KEY generated
- [ ] Supabase database URL ready
- [ ] Upstash Redis URL ready
- [ ] OpenRouter API key ready

After deployment:
- [ ] Health endpoint returns 200 OK
- [ ] API docs accessible
- [ ] No errors in deployment logs
- [ ] Database connection successful
- [ ] Redis connection successful
- [ ] Public URL copied

---

## 📝 Important Notes

1. **Root Directory**: Must be set to `backend` in Railway settings
2. **Imports**: All imports use `backend.` prefix (e.g., `from backend.api import router`)
3. **Port**: Railway automatically provides `$PORT` - do NOT set manually
4. **WebSockets**: Railway supports WebSockets by default - use `wss://` for secure connections
5. **CORS**: Configured to allow Vercel domains automatically

---

## 🆘 Troubleshooting

### Build Fails
- Check Root Directory is `backend`
- Verify `requirements.txt` exists
- Check Python version (3.11)

### Startup Fails
- Check environment variables are set
- Verify database connection string format
- Check Redis URL format
- Review deployment logs

### Import Errors
- Ensure Root Directory is `backend`
- Verify imports use `backend.` prefix

---

## 📚 Documentation

- Full deployment guide: `RAILWAY_DEPLOYMENT_GUIDE.md`
- Environment variables: `env.example.cloud`
- Backend README: `backend/README_RAILWAY.md`

---

**Status**: ✅ Backend ready for Railway deployment

**Next Step**: Follow Railway deployment instructions above, then proceed to frontend deployment.

