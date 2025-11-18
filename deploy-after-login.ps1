# ORIONX Deployment Script - Run AFTER railway login
# Usage: .\deploy-after-login.ps1 -ServiceName "your-service-name"

param(
    [Parameter(Mandatory=$true)]
    [string]$ServiceName
)

Write-Host "🚀 ORIONX Deployment - Post-Login" -ForegroundColor Cyan
Write-Host "===================================" -ForegroundColor Cyan
Write-Host ""

# Verify login
Write-Host "🔐 Verifying Railway login..." -ForegroundColor Yellow
$whoami = railway whoami 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Not logged in. Please run: railway login" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Logged in as: $($whoami -replace '.*@', '@')" -ForegroundColor Green
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

Write-Host "🔧 Pushing $($envVars.Count) environment variables..." -ForegroundColor Yellow
$success = 0
$failed = 0

foreach ($key in $envVars.Keys) {
    Write-Host "  $key..." -NoNewline -ForegroundColor Gray
    $result = railway variables set "$key=$($envVars[$key])" --service $ServiceName 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host " ✅" -ForegroundColor Green
        $success++
    } else {
        Write-Host " ❌" -ForegroundColor Red
        $failed++
    }
}

Write-Host ""
Write-Host "📊 Variables: $success success, $failed failed" -ForegroundColor $(if ($failed -eq 0) { "Green" } else { "Yellow" })
Write-Host ""

# Trigger deployment
Write-Host "🚀 Triggering deployment..." -ForegroundColor Yellow
railway up --service $ServiceName 2>&1 | Out-Null

Write-Host "⏳ Waiting 20 seconds for deployment to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 20

# Get URL
Write-Host "🔗 Getting backend URL..." -ForegroundColor Yellow
$domainInfo = railway domain --service $ServiceName 2>&1
$backendUrl = ""

if ($domainInfo -match "https://([\w-]+)\.up\.railway\.app") {
    $backendUrl = "https://$($matches[1]).up.railway.app"
} elseif ($domainInfo -match "https://.*\.railway\.app") {
    $backendUrl = ($domainInfo | Select-String -Pattern "https://.*\.railway\.app").Matches[0].Value
}

if ([string]::IsNullOrWhiteSpace($backendUrl)) {
    Write-Host "⚠️  Could not auto-detect URL" -ForegroundColor Yellow
    Write-Host "   Check Railway Dashboard > Settings > Networking > Public Domain" -ForegroundColor White
    $backendUrl = Read-Host "Enter Railway backend URL"
}

Write-Host "✅ Backend URL: $backendUrl" -ForegroundColor Green
$backendUrl | Out-File -FilePath "RAILWAY_BACKEND_URL.txt" -Encoding utf8

# Test health
Write-Host ""
Write-Host "🧪 Testing backend..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

try {
    $response = Invoke-RestMethod -Uri "$backendUrl/health" -Method GET -TimeoutSec 15
    Write-Host "✅ Health check: $($response.status)" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Health check failed (may still be deploying): $($_.Exception.Message)" -ForegroundColor Yellow
    Write-Host "   Wait a few minutes and test manually: curl $backendUrl/health" -ForegroundColor Gray
}

Write-Host ""
Write-Host "✅ Backend deployment complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Next: Update frontend and deploy to Vercel" -ForegroundColor Yellow
Write-Host "Backend URL saved to: RAILWAY_BACKEND_URL.txt" -ForegroundColor Gray

