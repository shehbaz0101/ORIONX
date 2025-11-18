# Script to create backend/.env from template
# Run this from the backend directory: .\create-env.ps1

$templateFile = "env.local.example"
$envFile = ".env"

if (Test-Path $templateFile) {
    Copy-Item $templateFile $envFile -Force
    Write-Host "✅ Created $envFile from $templateFile" -ForegroundColor Green
    Write-Host "⚠️  Remember to fill in actual values in $envFile" -ForegroundColor Yellow
} else {
    Write-Host "❌ Template file $templateFile not found" -ForegroundColor Red
    Write-Host "Please ensure you're in the backend directory" -ForegroundColor Yellow
}

