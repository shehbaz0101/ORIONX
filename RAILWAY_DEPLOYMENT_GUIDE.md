# ORIONX Backend - Railway Deployment Guide

## 📋 Prerequisites

1. **Railway Account**: Sign up at https://railway.app
2. **GitHub Account**: Your ORIONX repository must be on GitHub
3. **Environment Variables Ready**:
   - Supabase database connection string
   - Upstash Redis URL
   - OpenRouter API key
   - Secret key for JWT

---

## 🚀 Step-by-Step Deployment Instructions

### Step 1: Create New Railway Project

1. Go to https://railway.app and log in
2. Click **"New Project"** button (top right)
3. Select **"Deploy from GitHub repo"**
4. Authorize Railway to access your GitHub account (if first time)
5. Select your **ORIONX repository**
6. Railway will automatically detect it's a Python project

### Step 2: Configure Service Settings

1. In your Railway project, you'll see a service (likely named after your repo)
2. Click on the service to open settings
3. Go to **Settings** tab
4. Under **"Root Directory"**, set it to: `backend`
   - This tells Railway where your Python code is located
5. Click **"Save"**

### Step 3: Configure Build Settings

1. Still in **Settings** tab
2. Railway should auto-detect:
   - **Build Command**: `pip install -r requirements.txt` (automatic)
   - **Start Command**: Will use Procfile automatically
3. Verify **Procfile** is detected (should show: `web: uvicorn main:app --host 0.0.0.0 --port $PORT`)

### Step 4: Set Environment Variables

1. In your service, go to **Variables** tab
2. Click **"New Variable"** for each of the following:

#### Required Environment Variables:

```bash
# Database (Supabase)
SUPABASE_DB_URL=postgresql+asyncpg://postgres:[YOUR_PASSWORD]@db.[PROJECT_REF].supabase.co:5432/postgres

# Redis (Upstash)
UPSTASH_REDIS_URL=redis://default:[PASSWORD]@[ENDPOINT].upstash.io:[PORT]

# AI (OpenRouter)
OPENROUTER_API_KEY=sk-or-v1-[YOUR_API_KEY]

# Security
SECRET_KEY=[GENERATE_A_RANDOM_32_CHAR_STRING]

# Optional: Frontend Domain (for CORS)
FRONTEND_DOMAIN=app.orionx.ai
```

**To generate SECRET_KEY:**
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

3. Click **"Add"** after each variable
4. **Important**: Railway automatically provides `PORT` variable - do NOT set it manually

### Step 5: Deploy

1. Railway will automatically start deploying when you:
   - Push code to your GitHub repo, OR
   - Click **"Redeploy"** button in the **Deployments** tab
2. Go to **Deployments** tab to watch the build logs
3. Wait for deployment to complete (usually 2-5 minutes)

### Step 6: Verify Deployment Logs

1. In **Deployments** tab, click on the latest deployment
2. Check the logs for:
   - ✅ `Successfully installed` (dependencies)
   - ✅ `Starting ORIONX backend...`
   - ✅ `ORIONX backend started successfully`
   - ✅ `Application startup complete`
3. If you see errors:
   - Check environment variables are set correctly
   - Verify database connection string format
   - Check Redis URL format

### Step 7: Get Your Public URL

1. Go to **Settings** tab
2. Scroll to **"Networking"** section
3. Under **"Public Domain"**, you'll see your Railway URL:
   - Format: `https://[service-name].up.railway.app`
4. Copy this URL - this is your backend API URL

### Step 8: Test Deployment

#### Test Health Endpoint:
```bash
curl https://[YOUR_RAILWAY_URL].up.railway.app/health
```

Expected response:
```json
{"status": "healthy", "service": "ORIONX"}
```

#### Test API Docs:
Open in browser:
```
https://[YOUR_RAILWAY_URL].up.railway.app/docs
```

You should see the FastAPI Swagger UI with all endpoints.

#### Test Root Endpoint:
```bash
curl https://[YOUR_RAILWAY_URL].up.railway.app/
```

Expected response:
```json
{
  "message": "ORIONX API",
  "version": "1.0.0",
  "docs": "/docs"
}
```

---

## 🔧 Troubleshooting

### Build Fails

**Problem**: Build fails with import errors
- **Solution**: Verify Root Directory is set to `backend`
- Check that `requirements.txt` exists in backend folder
- Verify all Python imports use `backend.` prefix

**Problem**: Build fails with dependency errors
- **Solution**: Check `requirements.txt` for correct package versions
- Some packages may need system dependencies (handled by Nixpacks)

### Deployment Fails

**Problem**: Application crashes on startup
- **Check logs** in Deployments tab
- Verify all environment variables are set
- Check database connection string format (must include `+asyncpg`)
- Verify Redis URL format

**Problem**: "Module not found" errors
- **Solution**: Ensure Root Directory is `backend`
- Verify imports use `backend.` prefix (e.g., `from backend.api import router`)

### Database Connection Issues

**Problem**: Cannot connect to Supabase
- **Verify**: `SUPABASE_DB_URL` format:
  - Must be: `postgresql+asyncpg://postgres:[PASSWORD]@db.[PROJECT_REF].supabase.co:5432/postgres`
  - Replace `[PASSWORD]` with actual password
  - Replace `[PROJECT_REF]` with your Supabase project reference
- **Check**: Supabase database is running and accessible

### Redis Connection Issues

**Problem**: Cannot connect to Upstash Redis
- **Verify**: `UPSTASH_REDIS_URL` format:
  - Must be: `redis://default:[PASSWORD]@[ENDPOINT].upstash.io:[PORT]`
- **Check**: Upstash database is active

### WebSocket Issues

**Problem**: WebSocket connections fail
- **Verify**: Railway supports WebSockets (it does by default)
- **Check**: Frontend uses `wss://` (secure WebSocket) for production
- **Test**: WebSocket endpoint: `wss://[YOUR_RAILWAY_URL].up.railway.app/api/market/ws`

---

## 📝 Post-Deployment Checklist

- [ ] Health endpoint returns `{"status": "healthy"}`
- [ ] API docs accessible at `/docs`
- [ ] Root endpoint returns API info
- [ ] Database connection successful (check logs)
- [ ] Redis connection successful (check logs)
- [ ] All environment variables set correctly
- [ ] Public URL copied for frontend configuration

---

## 🔗 Next Steps

After successful backend deployment:

1. **Copy your Railway URL** (e.g., `https://orionx-backend.up.railway.app`)
2. **Update frontend environment variables**:
   - `NEXT_PUBLIC_API_URL=https://[YOUR_RAILWAY_URL].up.railway.app`
   - `NEXT_PUBLIC_WS_URL=wss://[YOUR_RAILWAY_URL].up.railway.app`
3. **Deploy frontend to Vercel** (see frontend deployment guide)

---

## 📊 Monitoring

### View Logs
- Go to **Deployments** tab
- Click on any deployment
- View real-time logs

### Metrics
- Go to **Metrics** tab
- Monitor:
  - CPU usage
  - Memory usage
  - Request count
  - Response times

### Alerts
- Set up alerts in Railway dashboard for:
  - High error rates
  - High resource usage
  - Deployment failures

---

## 🎯 Expected Deployment Output

After successful deployment, you should have:

- **Service Name**: `orionx-backend` (or your custom name)
- **Public API URL**: `https://[service-name].up.railway.app`
- **Health Check**: `https://[service-name].up.railway.app/health`
- **API Docs**: `https://[service-name].up.railway.app/docs`
- **WebSocket URL**: `wss://[service-name].up.railway.app/api/market/ws`

---

## ✅ Success Criteria

Your backend is successfully deployed when:

1. ✅ Health endpoint returns 200 OK
2. ✅ API docs page loads
3. ✅ No errors in deployment logs
4. ✅ Database connection successful
5. ✅ Redis connection successful
6. ✅ All endpoints accessible

---

**Ready to deploy?** Follow the steps above and verify each step before proceeding to the next!

