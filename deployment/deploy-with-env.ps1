param(
    [Parameter(Mandatory=$true)][string]$ResourceGroup,
    [Parameter(Mandatory=$true)][string]$WebAppName,
    [Parameter(Mandatory=$false)][string]$EnvFilePath = ".env"
)

function Write-Info { param([string]$Message); Write-Host "[INFO] $Message" -ForegroundColor Cyan }
function Write-Success { param([string]$Message); Write-Host "[OK] $Message" -ForegroundColor Green }
function Write-Error-Custom { param([string]$Message); Write-Host "[ERROR] $Message" -ForegroundColor Red }

Write-Host "`n=== ALMA Chatbot - Deploy FINAL (Persistence & Timeout Fix) ===" -ForegroundColor Magenta

# 1. Directory Setup
# Determine project root relative to this script
$scriptDir = $PSScriptRoot
$projectRoot = Split-Path -Parent $scriptDir

Write-Info "Script location: $scriptDir"
Write-Info "Project root determined as: $projectRoot"

# Move context to project root
Push-Location $projectRoot

$tempDir = Join-Path $env:TEMP "alma-deploy-clean"
if (Test-Path $tempDir) { Remove-Item $tempDir -Recurse -Force }
New-Item -ItemType Directory -Path $tempDir -Force | Out-Null

# 2. Copy Base Files (EXCLUDING .deployment to prevent unwanted builds)
Write-Info "Copying base files..."
if (Test-Path "requirements.txt") {
    Copy-Item "requirements.txt" (Join-Path $tempDir "requirements.txt")
} else {
    Write-Error-Custom "requirements.txt not found!"
    exit 1
}

# Handle startup script location
if (Test-Path "deployment/startup_azure.sh") {
    Copy-Item "deployment/startup_azure.sh" (Join-Path $tempDir "startup_azure.sh")
} elseif (Test-Path "startup_azure.sh") {
    Copy-Item "startup_azure.sh" (Join-Path $tempDir "startup_azure.sh")
} else {
    Write-Error-Custom "startup_azure.sh NOT FOUND!"
    exit 1
}

# 3. Copy APP (Backend)
Write-Info "Copying APP folder..."
if (Test-Path "app") {
    $appDest = Join-Path $tempDir "app"
    Copy-Item "app" $tempDir -Recurse -Force
} else {
    Write-Error-Custom "APP folder NOT FOUND in $projectRoot"
    exit 1
}

# 4. Copy FRONTEND
Write-Info "Copying FRONTEND folder..."
if (Test-Path "frontend") {
    Copy-Item "frontend" $tempDir -Recurse -Force
}

# 5. ZIP Package
$zipPath = Join-Path $env:TEMP "alma-deploy.zip"
if (Test-Path $zipPath) { Remove-Item $zipPath -Force }

Write-Info "Zipping package..."
Push-Location $tempDir
try { tar -a -cf $zipPath * } finally { Pop-Location }

# 6. Azure Configuration (CRITICAL SETTINGS)
Write-Info "Configuring Azure settings (Timeout & No-Build)..."

# We set SCM_DO_BUILD... to false to stop Oryx from failing.
# We set WEBSITES_CONTAINER_START_TIME_LIMIT to 1800 (30 mins) to allow heavy pip install.
$settings = @(
    "SCM_DO_BUILD_DURING_DEPLOYMENT=false",
    "ENABLE_ORYX_BUILD=false",
    "WEBSITES_CONTAINER_START_TIME_LIMIT=1800" 
)
az webapp config appsettings set --name $WebAppName --resource-group $ResourceGroup --settings $settings --output none

# 7. Deploy
Write-Info "Deploying ZIP to Azure ($WebAppName)..."
# We use config-zip to simply extract files to wwwroot without logic
az webapp deployment source config-zip --resource-group $ResourceGroup --name $WebAppName --src $zipPath

if ($LASTEXITCODE -eq 0) {
    Write-Success "Deploy Success! Triggering restart..."
    az webapp restart --name $WebAppName --resource-group $ResourceGroup --output none
    Write-Success "App restarted. NOTE: First startup will take ~5-10 minutes to install libraries."
} else {
    Write-Error-Custom "Deploy failed"
}

# Restore terminal location
Pop-Location