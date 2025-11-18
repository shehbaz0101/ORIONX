# ⚡ ORIONX Vercel Deployment - Step-by-Step Guide

## Prerequisites

- ✅ Backend deployed on Railway
- ✅ Railway backend URL obtained
- ✅ Vercel account created

---

## Step 1: Update Frontend Environment Variables

After backend is deployed, update `frontend/.env.production` with your Railway URL:

```env
NEXT_PUBLIC_API_URL=https://[YOUR_RAILWAY_URL].up.railway.app
NEXT_PUBLIC_SUPABASE_URL=https://fizlofuvxbdbbbqhjcgk.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZpemxvZnV2eGJkYmJicWhqY2drIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjM0NDE2MTEsImV4cCI6MjA3OTAxNzYxMX0.1FKznPfZjVn-HQf3nIyuIIXCp0zcKiiNoNuENlcPxFc
NEXT_PUBLIC_OPENROUTER_ENABLED=true
```

---

## Step 2: Create Vercel Project

1. Go to https://vercel.com
2. Click **"Add New"** > **"Project"**
3. Import your GitHub repository
4. Select **ORIONX** repository

---

## Step 3: Configure Build Settings

1. **Framework Preset**: Next.js (auto-detected)
2. **Root Directory**: `frontend/`
3. **Build Command**: `npm run build` (default)
4. **Output Directory**: `.next` (default)
5. **Install Command**: `npm install` (default)

---

## Step 4: Add Environment Variables

Go to **Environment Variables** and add:

### Variable 1: NEXT_PUBLIC_API_URL
- **Name**: `NEXT_PUBLIC_API_URL`
- **Value**: `https://[YOUR_RAILWAY_URL].up.railway.app`
- **Environment**: Production, Preview, Development
- Click **"Add"**

### Variable 2: NEXT_PUBLIC_SUPABASE_URL
- **Name**: `NEXT_PUBLIC_SUPABASE_URL`
- **Value**: `https://fizlofuvxbdbbbqhjcgk.supabase.co`
- **Environment**: Production, Preview, Development
- Click **"Add"**

### Variable 3: NEXT_PUBLIC_SUPABASE_ANON_KEY
- **Name**: `NEXT_PUBLIC_SUPABASE_ANON_KEY`
- **Value**: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZpemxvZnV2eGJkYmJicWhqY2drIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjM0NDE2MTEsImV4cCI6MjA3OTAxNzYxMX0.1FKznPfZjVn-HQf3nIyuIIXCp0zcKiiNoNuENlcPxFc`
- **Environment**: Production, Preview, Development
- Click **"Add"**

### Variable 4: NEXT_PUBLIC_OPENROUTER_ENABLED
- **Name**: `NEXT_PUBLIC_OPENROUTER_ENABLED`
- **Value**: `true`
- **Environment**: Production, Preview, Development
- Click **"Add"**

---

## Step 5: Deploy

1. Click **"Deploy"** button
2. Vercel will build and deploy automatically
3. Wait for deployment to complete (2-3 minutes)

---

## Step 6: Get Frontend URL

1. Once deployed, you'll see your Vercel URL
2. Format: `https://[project-name].vercel.app`
3. Copy this URL

---

## Step 7: Update Backend CORS (if needed)

If frontend can't connect to backend:

1. Go to Railway Dashboard
2. Service > Variables
3. Update `FRONTEND_DOMAIN` to your Vercel URL (without https://)
4. Redeploy backend

---

## Step 8: Test Frontend

1. Visit your Vercel URL
2. Check browser console for errors
3. Test:
   - Login/Register
   - API connectivity
   - WebSocket connections

---

## Troubleshooting

### Build Fails
- Check Root Directory is `frontend/`
- Verify `package.json` exists
- Check build logs for errors

### API Connection Fails
- Verify `NEXT_PUBLIC_API_URL` is correct
- Check backend CORS settings
- Verify backend is running

### WebSocket Fails
- Ensure `NEXT_PUBLIC_API_URL` uses `https://`
- WebSocket will automatically use `wss://`

