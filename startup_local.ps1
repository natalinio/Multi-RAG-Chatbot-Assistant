# Local Development Startup Script for CORTEX
# This script starts the application without --reload to avoid venv/ monitoring issues

Write-Host "🚀 Starting CORTEX locally..." -ForegroundColor Cyan

# Activate virtual environment
& ".\venv\Scripts\Activate.ps1"

# Start uvicorn without reload (use Ctrl+C and restart manually after code changes)
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000

# Note: For development with auto-reload, changes must be manually applied
# Azure deployment will use startup_azure.sh which never includes --reload
