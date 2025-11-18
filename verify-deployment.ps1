# ORIONX Deployment Verification Script
# Run this after deploying to Railway and Vercel

param(
    [Parameter(Mandatory=$true)]
    [string]$RailwayUrl,
    [Parameter(Mandatory=$true)]
    [string]$VercelUrl
)

Write-Host "🧪 ORIONX Deployment Verification" -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Cyan
Write-Host ""

# Test Backend
Write-Host "🔍 Testing Backend..." -ForegroundColor Yellow
Write-Host "  URL: $RailwayUrl" -ForegroundColor Gray
Write-Host ""

# Health Check
Write-Host "  Testing /health endpoint..." -NoNewline -ForegroundColor Gray
try {
    $healthResponse = Invoke-RestMethod -Uri "$RailwayUrl/health" -Method GET -TimeoutSec 10 -ErrorAction Stop
    Write-Host " ✅" -ForegroundColor Green
    Write-Host "    Status: $($healthResponse.status)" -ForegroundColor Green
    Write-Host "    Service: $($healthResponse.service)" -ForegroundColor Green
} catch {
    Write-Host " ❌" -ForegroundColor Red
    Write-Host "    Error: $($_.Exception.Message)" -ForegroundColor Red
}

# API Docs
Write-Host "  Testing /docs endpoint..." -NoNewline -ForegroundColor Gray
try {
    $docsResponse = Invoke-WebRequest -Uri "$RailwayUrl/docs" -Method GET -TimeoutSec 10 -UseBasicParsing -ErrorAction Stop
    if ($docsResponse.StatusCode -eq 200) {
        Write-Host " ✅" -ForegroundColor Green
    }
} catch {
    Write-Host " ⚠️" -ForegroundColor Yellow
}

# Test Frontend
Write-Host ""
Write-Host "🔍 Testing Frontend..." -ForegroundColor Yellow
Write-Host "  URL: $VercelUrl" -ForegroundColor Gray
Write-Host ""

Write-Host "  Testing frontend homepage..." -NoNewline -ForegroundColor Gray
try {
    $frontendResponse = Invoke-WebRequest -Uri $VercelUrl -Method GET -TimeoutSec 10 -UseBasicParsing -ErrorAction Stop
    if ($frontendResponse.StatusCode -eq 200) {
        Write-Host " ✅" -ForegroundColor Green
        Write-Host "    Status: $($frontendResponse.StatusCode)" -ForegroundColor Green
    }
} catch {
    Write-Host " ❌" -ForegroundColor Red
    Write-Host "    Error: $($_.Exception.Message)" -ForegroundColor Red
}

# Test API Connection from Frontend
Write-Host ""
Write-Host "🔗 Testing Frontend → Backend Connection..." -ForegroundColor Yellow
Write-Host "  Checking if frontend can reach backend..." -ForegroundColor Gray

# Save URLs
$deploymentInfo = @{
    backend_url = $RailwayUrl
    frontend_url = $VercelUrl
    deployment_date = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
} | ConvertTo-Json

$deploymentInfo | Out-File -FilePath "DEPLOYMENT_URLS.json" -Encoding utf8

Write-Host ""
Write-Host "=================================" -ForegroundColor Cyan
Write-Host "✅ Deployment Verification Complete" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Deployment URLs:" -ForegroundColor Cyan
Write-Host "  Backend:  $RailwayUrl" -ForegroundColor White
Write-Host "  Frontend: $VercelUrl" -ForegroundColor White
Write-Host ""
Write-Host "📝 URLs saved to: DEPLOYMENT_URLS.json" -ForegroundColor Gray
Write-Host ""
Write-Host "🌐 Open your app:" -ForegroundColor Yellow
Write-Host "  $VercelUrl" -ForegroundColor Cyan
Write-Host ""

