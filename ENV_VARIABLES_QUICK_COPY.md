# 📋 ORIONX Environment Variables - Quick Copy

## 🚀 Railway Backend Variables (11 total)

Copy each variable name and value, then paste into Railway Dashboard > Variables tab.

---

### Variable 1
**Name:**
```
SUPABASE_DB_URL
```

**Value:**
```
postgresql+asyncpg://postgres:Pulsar%40220@db.fizlofuvxbdbbbqhjcgk.supabase.co:5432/postgres?sslmode=require
```

---

### Variable 2
**Name:**
```
DATABASE_URL
```

**Value:**
```
postgresql+asyncpg://postgres:postgres@localhost:5432/orionx
```

---

### Variable 3
**Name:**
```
REDIS_URL
```

**Value:**
```
redis://default:ATtxAAIncDI0NmFiZDJhMTA1ZGQ0ZWRhODBlZmI2ZmQ2Y2JkNTJjMXAyMTUyMTc@electric-walrus-15217.upstash.io:6379
```

---

### Variable 4
**Name:**
```
UPSTASH_REDIS_URL
```

**Value:**
```
redis://localhost:6379/0
```

---

### Variable 5
**Name:**
```
OPENROUTER_API_KEY
```

**Value:**
```
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
```

---

### Variable 6
**Name:**
```
SECRET_KEY
```

**Value:**
```
aGohO5ZMAqH7Uel4Vr1LcyjznQW2siuRCFSIEfKTxtw
```

---

### Variable 7
**Name:**
```
SUPABASE_SERVICE_ROLE_KEY
```

**Value:**
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZpemxvZnV2eGJkYmJicWhqY2drIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2MzQ0MTYxMSwiZXhwIjoyMDc5MDE3NjExfQ.zE2ZnCP6xARgwc1htOZWiYyEvOtNP1kEo3csF_1s4s0
```

---

### Variable 8
**Name:**
```
SUPABASE_PROJECT_URL
```

**Value:**
```
https://fizlofuvxbdbbbqhjcgk.supabase.co
```

---

### Variable 9
**Name:**
```
SUPABASE_ANON_KEY
```

**Value:**
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZpemxvZnV2eGJkYmJicWhqY2drIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjM0NDE2MTEsImV4cCI6MjA3OTAxNzYxMX0.1FKznPfZjVn-HQf3nIyuIIXCp0zcKiiNoNuENlcPxFc
```

---

### Variable 10
**Name:**
```
CORS_ORIGINS
```

**Value:**
```
*
```

---

### Variable 11
**Name:**
```
FRONTEND_DOMAIN
```

**Value:**
```
*
```

---

## 📝 How to Use

1. Go to Railway Dashboard
2. Click on your service
3. Go to **Variables** tab
4. Click **"New Variable"**
5. Copy **Name** from above → paste in Name field
6. Copy **Value** from above → paste in Value field
7. Click **Add**
8. Repeat for all 11 variables

---

## ✅ Checklist

- [ ] SUPABASE_DB_URL
- [ ] DATABASE_URL
- [ ] REDIS_URL
- [ ] UPSTASH_REDIS_URL
- [ ] OPENROUTER_API_KEY
- [ ] SECRET_KEY
- [ ] SUPABASE_SERVICE_ROLE_KEY
- [ ] SUPABASE_PROJECT_URL
- [ ] SUPABASE_ANON_KEY
- [ ] CORS_ORIGINS
- [ ] FRONTEND_DOMAIN

---

## 🎯 Vercel Frontend Variables (After Backend Deploys)

Once you have your Railway backend URL, add these to Vercel:

### Variable 1
**Name:** `NEXT_PUBLIC_API_URL`  
**Value:** `https://[YOUR_RAILWAY_URL].up.railway.app`

### Variable 2
**Name:** `NEXT_PUBLIC_SUPABASE_URL`  
**Value:** `https://fizlofuvxbdbbbqhjcgk.supabase.co`

### Variable 3
**Name:** `NEXT_PUBLIC_SUPABASE_ANON_KEY`  
**Value:** `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZpemxvZnV2eGJkYmJicWhqY2drIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjM0NDE2MTEsImV4cCI6MjA3OTAxNzYxMX0.1FKznPfZjVn-HQf3nIyuIIXCp0zcKiiNoNuENlcPxFc`

### Variable 4
**Name:** `NEXT_PUBLIC_OPENROUTER_ENABLED`  
**Value:** `true`

---

**Quick and easy! Just copy-paste! 🚀**

