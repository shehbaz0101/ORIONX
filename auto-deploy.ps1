# ORIONX Automated Deployment Script
# This script handles the complete deployment process

Write-Host "🚀 ORIONX Automated Deployment" -ForegroundColor Cyan
Write-Host "===============================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Check Railway CLI
Write-Host "📦 Checking Railway CLI..." -ForegroundColor Yellow
$railwayInstalled = Get-Command railway -ErrorAction SilentlyContinue
if (-not $railwayInstalled) {
    Write-Host "❌ Railway CLI not found. Installing..." -ForegroundColor Red
    npm install -g @railway/cli
    Start-Sleep -Seconds 3
}

Write-Host "✅ Railway CLI ready" -ForegroundColor Green
Write-Host ""

# Step 2: Check login
Write-Host "🔐 Checking Railway login..." -ForegroundColor Yellow
$loginCheck = railway whoami 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "⚠️  Not logged in to Railway" -ForegroundColor Yellow
    Write-Host "🔑 Opening Railway login..." -ForegroundColor Yellow
    Write-Host "   Please complete login in the browser window that opens." -ForegroundColor White
    Write-Host ""
    railway login
    Write-Host ""
    Write-Host "⏳ Waiting for login to complete..." -ForegroundColor Yellow
    Start-Sleep -Seconds 5
    
    # Verify login
    $loginCheck = railway whoami 2>&1
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Login failed. Please run 'railway login' manually and try again." -ForegroundColor Red
        exit 1
    }
}

Write-Host "✅ Logged in to Railway" -ForegroundColor Green
$user = railway whoami 2>&1 | Select-String -Pattern "@" | ForEach-Object { $_.Line }
Write-Host "   User: $user" -ForegroundColor Gray
Write-Host ""

# Step 3: List projects to find ORIONX
Write-Host "🔍 Finding Railway project..." -ForegroundColor Yellow
$projects = railway list 2>&1

if ($LASTEXITCODE -ne 0) {
    Write-Host "⚠️  Could not list projects. Checking if we need to link..." -ForegroundColor Yellow
    Write-Host "   Please ensure you have created a Railway project for ORIONX" -ForegroundColor White
    Write-Host "   Go to: https://railway.app > New Project > Deploy from GitHub" -ForegroundColor White
    Write-Host ""
    
    # Try to link
    Write-Host "🔗 Attempting to link project..." -ForegroundColor Yellow
    railway link
}

Write-Host ""

# Step 4: Get service name
Write-Host "📋 Please provide your Railway service name:" -ForegroundColor Yellow
Write-Host "   (This is the name shown in Railway Dashboard for your backend service)" -ForegroundColor Gray
$serviceName = Read-Host "Service name"

if ([string]::IsNullOrWhiteSpace($serviceName)) {
    Write-Host "❌ Service name is required" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "🔧 Pushing environment variables to Railway..." -ForegroundColor Yellow
Write-Host ""

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
$failCount = 0

foreach ($key in $envVars.Keys) {
    $value = $envVars[$key]
    Write-Host "  Setting $key..." -ForegroundColor Gray -NoNewline
    
    $result = railway variables set "$key=$value" --service $serviceName 2>&1
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host " ✅" -ForegroundColor Green
        $successCount++
    } else {
        Write-Host " ❌" -ForegroundColor Red
        Write-Host "    Error: $result" -ForegroundColor Red
        $failCount++
    }
}

Write-Host ""
Write-Host "📊 Variables Summary:" -ForegroundColor Cyan
Write-Host "  ✅ Success: $successCount" -ForegroundColor Green
Write-Host "  ❌ Failed: $failCount" -ForegroundColor $(if ($failCount -gt 0) { "Red" } else { "Green" })
Write-Host ""

if ($failCount -gt 0) {
    Write-Host "⚠️  Some variables failed. Please check Railway Dashboard." -ForegroundColor Yellow
    Write-Host "   You may need to set them manually in Railway > Settings > Variables" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "🚀 Triggering deployment..." -ForegroundColor Yellow

# Trigger deployment
railway up --service $serviceName 2>&1

Write-Host ""
Write-Host "⏳ Deployment started. Checking status..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

# Get service URL
Write-Host ""
Write-Host "🔗 Getting Railway service URL..." -ForegroundColor Yellow
$serviceUrl = railway domain --service $serviceName 2>&1

if ($serviceUrl -match "https://.*\.up\.railway\.app") {
    $backendUrl = $matches[0]
    Write-Host "✅ Backend URL: $backendUrl" -ForegroundColor Green
    Write-Host ""
    Write-Host "📝 Saving backend URL..." -ForegroundColor Yellow
    
    # Save to file
    $backendUrl | Out-File -FilePath "backend-url.txt" -Encoding utf8
    
    Write-Host "✅ Backend URL saved to backend-url.txt" -ForegroundColor Green
} else {
    Write-Host "⚠️  Could not get URL automatically. Please check Railway Dashboard > Settings > Networking" -ForegroundColor Yellow
    Write-Host "   Look for 'Public Domain' section" -ForegroundColor White
}

Write-Host ""
Write-Host "✅ Phase 1 Complete: Backend deployment initiated" -ForegroundColor Green
Write-Host ""
Write-Host "Next: Update frontend env and deploy to Vercel" -ForegroundColor Yellow

