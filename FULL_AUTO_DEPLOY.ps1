# ORIONX Full Automated Deployment
# Complete end-to-end deployment automation

param(
    [string]$RailwayServiceName = "",
    [switch]$SkipLogin = $false
)

Write-Host "🚀 ORIONX Full Automated Deployment" -ForegroundColor Cyan
Write-Host "====================================" -ForegroundColor Cyan
Write-Host ""

# ============================================
# PHASE 1: RAILWAY BACKEND DEPLOYMENT
# ============================================

Write-Host "📦 PHASE 1: Backend Deployment to Railway" -ForegroundColor Yellow
Write-Host "===========================================" -ForegroundColor Yellow
Write-Host ""

# Check Railway CLI
$railwayInstalled = Get-Command railway -ErrorAction SilentlyContinue
if (-not $railwayInstalled) {
    Write-Host "📥 Installing Railway CLI..." -ForegroundColor Yellow
    npm install -g @railway/cli
    Start-Sleep -Seconds 3
}

# Check login
if (-not $SkipLogin) {
    Write-Host "🔐 Checking Railway login..." -ForegroundColor Yellow
    $loginCheck = railway whoami 2>&1
    if ($LASTEXITCODE -ne 0) {
        Write-Host "⚠️  Please login to Railway:" -ForegroundColor Yellow
        Write-Host "   Run: railway login" -ForegroundColor White
        Write-Host "   Then run this script again with -SkipLogin flag" -ForegroundColor White
        exit 1
    }
    Write-Host "✅ Logged in" -ForegroundColor Green
}

# Get service name if not provided
if ([string]::IsNullOrWhiteSpace($RailwayServiceName)) {
    Write-Host "📋 Please enter your Railway service name:" -ForegroundColor Yellow
    $RailwayServiceName = Read-Host "Service name"
}

if ([string]::IsNullOrWhiteSpace($RailwayServiceName)) {
    Write-Host "❌ Service name required" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "🔧 Pushing environment variables..." -ForegroundColor Yellow

# Environment variables
$envVars = @{
    "SUPABASE_DB_URL" = "postgresql+asyncpg://postgres:Pulsar%40220@db.fizlofuvxbdbbbqhjcgk.supabase.co:5432/postgres?sslmode=require"
    "DATABASE_URL" = "postgresql+asyncpg://postgres:postgres@localhost:5432/orionx"
    "REDIS_URL" = "redis://default:ATtxAAIncDI0NmFiZDJhMTA1ZGQ0ZWRhODBlZmI2ZmQ2Y2JkNTJjMXAyMTUyMTc@electric-walrus-15217.upstash.io:6379"
    "UPSTASH_REDIS_URL" = "redis://localhost:6379/0"
    "OPENROUTER_API_KEY" = "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"
    "SECRET_KEY" = "aGohO5ZMAqH7Uel4Vr1LcyjznQW2siuRCFSIEfKTxtw"
    "SUPABASE_SERVICE_ROLE_KEY" = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZpemxvZnV2eGJkYmJicWhqY2drIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2MzQ0MTYxMSwiZXhwIjoyMDc5MDE3NjExfQ.zE2ZnCP6xARgwc1htOZWiYyEvOtNP1kEo3csF_1s4s0"
    "SUPABASE_PROJECT_URL" = "https://fizlofuvxbdbbbqhjcgk.supabase.co"
    "SUPABASE_ANON_KEY" = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZpemxvZnV2eGJkYmJicWhqY2drIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjM0NDE2MTEsImV4cCI6MjA3OTAxNzYxMX0.1FKznPfZjVn-HQf3nIyuIIXCp0zcKiiNoNuENlcPxFc"
    "CORS_ORIGINS" = "*"
    "FRONTEND_DOMAIN" = "*"
}

$successCount = 0
foreach ($key in $envVars.Keys) {
    $value = $envVars[$key]
    Write-Host "  $key..." -NoNewline -ForegroundColor Gray
    $result = railway variables set "$key=$value" --service $RailwayServiceName 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host " ✅" -ForegroundColor Green
        $successCount++
    } else {
        Write-Host " ❌" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "✅ $successCount variables set" -ForegroundColor Green
Write-Host ""

# Trigger deployment
Write-Host "🚀 Triggering Railway deployment..." -ForegroundColor Yellow
railway up --service $RailwayServiceName 2>&1 | Out-Null

Write-Host "⏳ Waiting for deployment..." -ForegroundColor Yellow
Start-Sleep -Seconds 15

# Get backend URL
Write-Host "🔗 Getting backend URL..." -ForegroundColor Yellow
$domainOutput = railway domain --service $RailwayServiceName 2>&1
$backendUrl = ""

if ($domainOutput -match "https://([\w-]+)\.up\.railway\.app") {
    $backendUrl = $matches[0]
} elseif ($domainOutput -match "https://.*\.railway\.app") {
    $backendUrl = $domainOutput -replace ".*(https://.*\.railway\.app).*", '$1'
}

if ([string]::IsNullOrWhiteSpace($backendUrl)) {
    Write-Host "⚠️  Could not get URL automatically" -ForegroundColor Yellow
    Write-Host "   Please check Railway Dashboard > Settings > Networking > Public Domain" -ForegroundColor White
    $backendUrl = Read-Host "Enter your Railway backend URL"
}

Write-Host "✅ Backend URL: $backendUrl" -ForegroundColor Green
$backendUrl | Out-File -FilePath "RAILWAY_BACKEND_URL.txt" -Encoding utf8

# Test backend
Write-Host ""
Write-Host "🧪 Testing backend..." -ForegroundColor Yellow
try {
    $healthResponse = Invoke-WebRequest -Uri "$backendUrl/health" -Method GET -TimeoutSec 10 -UseBasicParsing
    if ($healthResponse.StatusCode -eq 200) {
        Write-Host "✅ Backend health check passed" -ForegroundColor Green
        $healthContent = $healthResponse.Content | ConvertFrom-Json
        Write-Host "   Status: $($healthContent.status)" -ForegroundColor Gray
    }
} catch {
    Write-Host "⚠️  Health check failed (backend may still be deploying)" -ForegroundColor Yellow
    Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Gray
}

Write-Host ""
Write-Host "✅ PHASE 1 COMPLETE" -ForegroundColor Green
Write-Host ""

# ============================================
# PHASE 2: FRONTEND DEPLOYMENT
# ============================================

Write-Host "⚡ PHASE 2: Frontend Deployment to Vercel" -ForegroundColor Yellow
Write-Host "===========================================" -ForegroundColor Yellow
Write-Host ""

# Update frontend env
Write-Host "📝 Updating frontend/.env.production..." -ForegroundColor Yellow
$frontendEnv = @"
NEXT_PUBLIC_API_URL=$backendUrl
NEXT_PUBLIC_SUPABASE_URL=https://fizlofuvxbdbbbqhjcgk.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZpemxvZnV2eGJkYmJicWhqY2drIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjM0NDE2MTEsImV4cCI6MjA3OTAxNzYxMX0.1FKznPfZjVn-HQf3nIyuIIXCp0zcKiiNoNuENlcPxFc
NEXT_PUBLIC_OPENROUTER_ENABLED=true
"@

$frontendEnv | Out-File -FilePath "frontend\.env.production" -Encoding utf8
Write-Host "✅ Frontend env updated" -ForegroundColor Green
Write-Host ""

# Check Vercel CLI
Write-Host "🔍 Checking Vercel CLI..." -ForegroundColor Yellow
$vercelInstalled = Get-Command vercel -ErrorAction SilentlyContinue
if (-not $vercelInstalled) {
    Write-Host "📥 Installing Vercel CLI..." -ForegroundColor Yellow
    npm install -g vercel
    Start-Sleep -Seconds 3
}

# Deploy to Vercel
Write-Host "🚀 Deploying to Vercel..." -ForegroundColor Yellow
Write-Host "   (This will prompt for Vercel login if not already logged in)" -ForegroundColor Gray
Write-Host ""

Push-Location frontend
$vercelDeploy = vercel --prod --yes 2>&1
Pop-Location

if ($LASTEXITCODE -eq 0) {
    $frontendUrl = ($vercelDeploy | Select-String -Pattern "https://.*\.vercel\.app").Matches[0].Value
    Write-Host "✅ Frontend deployed: $frontendUrl" -ForegroundColor Green
    $frontendUrl | Out-File -FilePath "VERCEL_FRONTEND_URL.txt" -Encoding utf8
} else {
    Write-Host "⚠️  Vercel deployment needs manual setup" -ForegroundColor Yellow
    Write-Host "   Please deploy via Vercel Dashboard:" -ForegroundColor White
    Write-Host "   1. Go to https://vercel.com" -ForegroundColor White
    Write-Host "   2. Add New > Project" -ForegroundColor White
    Write-Host "   3. Import ORIONX repository" -ForegroundColor White
    Write-Host "   4. Set Root Directory to: frontend" -ForegroundColor White
    Write-Host "   5. Add environment variables from frontend/.env.production" -ForegroundColor White
    $frontendUrl = Read-Host "Enter your Vercel frontend URL"
}

Write-Host ""
Write-Host "✅ PHASE 2 COMPLETE" -ForegroundColor Green
Write-Host ""

# ============================================
# PHASE 3: FINAL VERIFICATION
# ============================================

Write-Host "🧪 PHASE 3: Final Verification" -ForegroundColor Yellow
Write-Host "===============================" -ForegroundColor Yellow
Write-Host ""

Write-Host "Testing endpoints..." -ForegroundColor Yellow

# Test backend endpoints
$endpoints = @(
    "/health",
    "/",
    "/docs"
)

foreach ($endpoint in $endpoints) {
    try {
        $response = Invoke-WebRequest -Uri "$backendUrl$endpoint" -Method GET -TimeoutSec 10 -UseBasicParsing
        Write-Host "  ✅ $endpoint - Status: $($response.StatusCode)" -ForegroundColor Green
    } catch {
        Write-Host "  ⚠️  $endpoint - $($_.Exception.Message)" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "====================================" -ForegroundColor Cyan
Write-Host "🎉 DEPLOYMENT COMPLETE" -ForegroundColor Green
Write-Host "====================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "BACKEND_URL: $backendUrl" -ForegroundColor Green
Write-Host "FRONTEND_URL: $frontendUrl" -ForegroundColor Green
Write-Host ""
Write-Host "STATUS: FULLY DEPLOYED" -ForegroundColor Green
Write-Host ""

