# Azure Deployment Directory
# CORTEX - Cognitive Orchestration & Retrieval Technology EXpert

This directory contains the automated deployment script and documentation for deploying CORTEX to Azure App Service.

## 📁 Files Overview

### Core Deployment Files
- **`deploy-with-env.ps1`** - Main automated deployment script (tested and validated)
- **`DEPLOYMENT_GUIDE.md`** - Complete step-by-step deployment guide

### Prerequisites
✅ Azure CLI installed and logged in
✅ Azure subscription access  
✅ Existing Azure resources (OpenAI, Cosmos DB, AI Search)
✅ `.env` file configured in project root

## 🚀 Quick Deploy (5 minutes)

```powershell
# 1. Navigate to deployment directory
cd deployment

# 2. Run the automated script
.\deploy-with-env.ps1 -ResourceGroup "Your-RG" -WebAppName "your-app-name"

# Example:
.\deploy-with-env.ps1 -ResourceGroup "West-EU-Datadistillery-GDA-DEV" -WebAppName "app-gda-chatbot-dev"
```

## 📖 Complete Documentation

For detailed instructions, prerequisites, troubleshooting, and configuration options, see:

**📋 [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)**

## ✅ What Gets Deployed

The script automatically packages and deploys:
- Backend API (`app/` directory)
- Frontend web interface (`frontend/` directory) 
- Python dependencies (`requirements.txt`)
- Startup configuration (`startup_azure.sh`)
- Environment variables (from `.env` file)

## 🔧 Script Features

- ✅ Reads configuration from `.env` file
- ✅ Creates clean deployment package
- ✅ Configures Azure App Service settings
- ✅ Handles timeout and build settings
- ✅ Performs ZIP deployment
- ✅ Restarts app automatically

## 💡 Environment Variables Required

Create `.env` in project root with:
```env
AZURE_OPENAI_API_KEY=your_key
AZURE_OPENAI_ENDPOINT=https://your-openai.cognitiveservices.azure.com/
COSMOS_DB_ENDPOINT=https://your-cosmos.documents.azure.com:443/
COSMOS_DB_KEY=your_key
AZURE_AI_SEARCH_ENDPOINT=https://your-search.search.windows.net
AZURE_AI_SEARCH_KEY=your_key
# ... additional variables (see DEPLOYMENT_GUIDE.md)
```

## 🆘 Issues?

1. Check **[DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)** troubleshooting section
2. Verify all Azure services are configured
3. Ensure `.env` file contains all required variables
4. Check logs: `az webapp log tail --name your-app --resource-group your-rg`
