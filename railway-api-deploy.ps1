# ORIONX Railway Deployment via REST API
# This uses Railway API token instead of CLI login

param(
    [Parameter(Mandatory=$true)]
    [string]$RailwayApiToken,
    [Parameter(Mandatory=$true)]
    [string]$ProjectId,
    [Parameter(Mandatory=$true)]
    [string]$ServiceId
)

Write-Host "🚀 ORIONX Railway Deployment via API" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

# Railway API base URL
$apiBase = "https://api.railway.app/v1"

# Headers
$headers = @{
    "Authorization" = "Bearer $RailwayApiToken"
    "Content-Type" = "application/json"
}

Write-Host "🔧 Setting environment variables via API..." -ForegroundColor Yellow
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
    Write-Host "  Setting $key..." -NoNewline -ForegroundColor Gray
    
    # Railway API endpoint for setting variables
    $body = @{
        name = $key
        value = $value
    } | ConvertTo-Json
    
    try {
        $response = Invoke-RestMethod -Uri "$apiBase/services/$ServiceId/variables" -Method POST -Headers $headers -Body $body -ErrorAction Stop
        Write-Host " ✅" -ForegroundColor Green
        $successCount++
    } catch {
        # Try update if exists
        try {
            $updateBody = @{
                value = $value
            } | ConvertTo-Json
            Invoke-RestMethod -Uri "$apiBase/services/$ServiceId/variables/$key" -Method PATCH -Headers $headers -Body $updateBody -ErrorAction Stop
            Write-Host " ✅" -ForegroundColor Green
            $successCount++
        } catch {
            Write-Host " ❌" -ForegroundColor Red
            Write-Host "    Error: $($_.Exception.Message)" -ForegroundColor Red
            $failCount++
        }
    }
}

Write-Host ""
Write-Host "📊 Variables: $successCount success, $failCount failed" -ForegroundColor $(if ($failCount -eq 0) { "Green" } else { "Yellow" })

# Trigger deployment
Write-Host ""
Write-Host "🚀 Triggering deployment..." -ForegroundColor Yellow
try {
    $deployBody = @{
        serviceId = $ServiceId
    } | ConvertTo-Json
    
    $deployResponse = Invoke-RestMethod -Uri "$apiBase/deployments" -Method POST -Headers $headers -Body $deployBody -ErrorAction Stop
    Write-Host "✅ Deployment triggered" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Could not trigger via API. Deploy manually via Railway Dashboard" -ForegroundColor Yellow
}

# Get service URL
Write-Host ""
Write-Host "🔗 Getting service URL..." -ForegroundColor Yellow
try {
    $serviceInfo = Invoke-RestMethod -Uri "$apiBase/services/$ServiceId" -Method GET -Headers $headers -ErrorAction Stop
    if ($serviceInfo.service.domain) {
        $backendUrl = "https://$($serviceInfo.service.domain)"
        Write-Host "✅ Backend URL: $backendUrl" -ForegroundColor Green
        $backendUrl | Out-File -FilePath "RAILWAY_BACKEND_URL.txt" -Encoding utf8
    }
} catch {
    Write-Host "⚠️  Could not get URL via API. Check Railway Dashboard" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "✅ Deployment initiated!" -ForegroundColor Green

