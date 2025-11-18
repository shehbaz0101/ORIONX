# ORIONX Railway Deployment Script
# This script pushes all environment variables to Railway

Write-Host "🚀 ORIONX Railway Deployment Script" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

# Check if Railway CLI is installed
$railwayInstalled = Get-Command railway -ErrorAction SilentlyContinue
if (-not $railwayInstalled) {
    Write-Host "❌ Railway CLI not found!" -ForegroundColor Red
    Write-Host "📥 Installing Railway CLI..." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Please install Railway CLI first:" -ForegroundColor Yellow
    Write-Host "  Option 1: npm install -g @railway/cli" -ForegroundColor White
    Write-Host "  Option 2: Download from https://railway.app/cli" -ForegroundColor White
    Write-Host ""
    Write-Host "After installation, run this script again." -ForegroundColor Yellow
    exit 1
}

Write-Host "✅ Railway CLI found" -ForegroundColor Green
Write-Host ""

# Check if logged in
Write-Host "🔐 Checking Railway login status..." -ForegroundColor Yellow
$loginCheck = railway whoami 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Not logged in to Railway" -ForegroundColor Red
    Write-Host "🔑 Please login first: railway login" -ForegroundColor Yellow
    exit 1
}

Write-Host "✅ Logged in to Railway" -ForegroundColor Green
Write-Host ""

# Get project/service name
Write-Host "📋 Please provide your Railway service name:" -ForegroundColor Yellow
Write-Host "   (This is the name of your backend service in Railway)" -ForegroundColor Gray
$serviceName = Read-Host "Service name"

if ([string]::IsNullOrWhiteSpace($serviceName)) {
    Write-Host "❌ Service name is required" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "🔧 Setting environment variables..." -ForegroundColor Yellow
Write-Host ""

# Environment variables to set
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
    
    # Railway CLI command to set variable
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
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "📊 Summary:" -ForegroundColor Cyan
Write-Host "  ✅ Success: $successCount" -ForegroundColor Green
Write-Host "  ❌ Failed: $failCount" -ForegroundColor $(if ($failCount -gt 0) { "Red" } else { "Green" })
Write-Host ""

if ($failCount -eq 0) {
    Write-Host "🎉 All environment variables set successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Yellow
    Write-Host "  1. Go to Railway Dashboard" -ForegroundColor White
    Write-Host "  2. Verify variables in Settings > Variables" -ForegroundColor White
    Write-Host "  3. Trigger deployment or push code to GitHub" -ForegroundColor White
} else {
    Write-Host "⚠️  Some variables failed to set. Please check Railway Dashboard manually." -ForegroundColor Yellow
}

