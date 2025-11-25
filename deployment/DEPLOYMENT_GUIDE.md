# 🚀 ALMA ETL Chatbot - Azure Deployment Guide

Complete guide for deploying ALMA to Azure App Service using the automated PowerShell script.

---

## 📋 Prerequisites

### Required Software
- **Azure CLI** 2.77.0 or higher ([Download here](https://docs.microsoft.com/cli/azure/install-azure-cli))
- **PowerShell** 5.1 or higher (Windows) / PowerShell Core (cross-platform)
- **Git** (for repository management)

### Required Azure Resources
Before deployment, ensure you have these Azure services already configured:

✅ **Azure OpenAI Service**
- GPT-4o model deployed
- text-embedding-3-small model deployed
- Endpoint URL and API key

✅ **Azure Cosmos DB** (SQL API)
- Database: `metadata`
- Container: `configurations`
- Endpoint URL and primary key

✅ **Azure AI Search**
- Index: `cpgai-gda-version` (populated with ETL documentation)
- Semantic configuration enabled
- Endpoint URL and admin key

---

## 🎯 Automated Deployment (Recommended)

The project includes a validated PowerShell script that handles the complete deployment process.

### Step 1: Prepare Environment File

Create a `.env` file in the project root with your Azure credentials:

```env
# Azure OpenAI
AZURE_OPENAI_API_KEY=your_openai_key
AZURE_OPENAI_ENDPOINT=https://your-openai.cognitiveservices.azure.com/
AZURE_OPENAI_API_VERSION=2025-01-01-preview
AZURE_OPENAI_CHAT_MODEL_NAME=gpt-4o
AZURE_OPENAI_EMBEDDING_MODEL_NAME=text-embedding-3-small

# Azure Cosmos DB
COSMOS_DB_ENDPOINT=https://your-cosmos.documents.azure.com:443/
COSMOS_DB_KEY=your_cosmos_key
COSMOS_DB_DATABASE_NAME=metadata
COSMOS_DB_CONTAINER_NAME=configurations

# Azure AI Search
AZURE_AI_SEARCH_ENDPOINT=https://your-search.search.windows.net
AZURE_AI_SEARCH_KEY=your_search_key
AZURE_AI_SEARCH_INDEX_NAME=cpgai-gda-version

# Application Settings
ENVIRONMENT=production
LOG_LEVEL=INFO
CORS_ORIGINS=*
```

### Step 2: Login to Azure

```powershell
# Login to Azure
az login

# Set your subscription (optional)
az account set --subscription "Your-Subscription-Name-or-ID"

# Verify login
az account show
```

### Step 3: Run Deployment Script

```powershell
# Navigate to deployment directory
cd deployment

# Execute the automated deployment
.\deploy-with-env.ps1 -ResourceGroup "Your-Resource-Group" -WebAppName "your-app-name"
```

**Example:**
```powershell
.\deploy-with-env.ps1 -ResourceGroup "West-EU-Datadistillery-GDA-DEV" -WebAppName "app-gda-chatbot-dev"
```

### What the Script Does

The `deploy-with-env.ps1` script automates the entire deployment process:

1. **Environment Setup**: Reads `.env` file and prepares project structure
2. **Package Creation**: Creates a clean deployment package with:
   - `app/` directory (backend code)
   - `frontend/` directory (web interface)
   - `requirements.txt` (Python dependencies)
   - `startup_azure.sh` (startup script)
3. **Azure Configuration**: Sets critical App Service settings:
   - `SCM_DO_BUILD_DURING_DEPLOYMENT=false`
   - `ENABLE_ORYX_BUILD=false`
   - `WEBSITES_CONTAINER_START_TIME_LIMIT=1800`
4. **ZIP Deployment**: Uses `az webapp deployment source config-zip`
5. **App Restart**: Restarts the App Service to apply changes

---

## ✅ Deployment Verification

### Step 1: Check Health Endpoint

```powershell
# Replace with your actual app name
$appName = "your-app-name"
curl "https://$appName.azurewebsites.net/api/health"
```

**Expected Response:**
```json
{
  "status": "healthy",
  "message": "ETL Assistant API is running",
  "kernel_available": true,
  "active_sessions": 0
}
```

### Step 2: Test Web Interface

Open your browser and navigate to:
```
https://your-app-name.azurewebsites.net/
```

### Step 3: Test API Documentation

```
https://your-app-name.azurewebsites.net/docs
```

### Step 4: Functional Tests

Try these chat interactions:

1. **ALMA Personality Test**
   - Ask: "Who are you?"
   - Expected: ALMA introduces herself with personality traits

2. **RAG Documentation Test**
   - Ask: "How to configure Bronze layer ingestion?"
   - Expected: Detailed response with documentation references

3. **Cosmos DB Query Test**
   - Ask: "Show me a NielsenGB configuration"
   - Expected: JSON configuration returned

4. **Counting Feature Test**
   - Ask: "How many configurations for NielsenGB?"
   - Expected: "110 configurations across 5 markets"

---

## 🔍 Troubleshooting

### Common Issues

#### Issue: 502 Bad Gateway
**Cause**: App is still starting up (first boot takes 5-10 minutes)
**Solution**: Wait 3-5 minutes, then check logs

```powershell
az webapp log tail --name your-app-name --resource-group Your-Resource-Group
```

#### Issue: ImportError with openai._types.omit
**Cause**: Incorrect openai version (< 1.109.0)
**Solution**: Verify `requirements.txt` contains `semantic-kernel[openai]==1.38.0`

#### Issue: Environment Variables Missing
**Cause**: `.env` file not found or incorrectly formatted
**Solution**: 
1. Verify `.env` exists in project root
2. Check all required variables are set
3. Re-run deployment script

#### Issue: Azure CLI Not Logged In
**Cause**: Azure CLI session expired
**Solution**:
```powershell
az login
az account set --subscription "Your-Subscription"
```

### Viewing Logs

```powershell
# Real-time logs
az webapp log tail --name your-app-name --resource-group Your-Resource-Group

# Download logs
az webapp log download --name your-app-name --resource-group Your-Resource-Group --log-file logs.zip

# Kudu console (advanced)
# https://your-app-name.scm.azurewebsites.net/
```

---

## 🔄 Updating the Application

To deploy code changes:

1. Make your code changes locally
2. Test locally (optional but recommended)
3. Re-run the deployment script:

```powershell
.\deploy-with-env.ps1 -ResourceGroup "Your-Resource-Group" -WebAppName "your-app-name"
```

The script will overwrite the previous deployment with the new version.

---

## 📊 Infrastructure Details

### App Service Configuration

The deployment creates/configures:

- **App Service Plan**: Linux, Python 3.11
- **Web App**: Configured for FastAPI with Uvicorn
- **Startup Command**: Uses `startup_azure.sh`
- **Environment Variables**: Copied from `.env` file
- **Build Settings**: Oryx build disabled for faster deployment

### Cost Estimation (Monthly)

| Service | SKU | Estimated Cost |
|---------|-----|----------------|
| App Service Plan | B1 Basic | €13 |
| Azure OpenAI | Pay-per-use | €50-200 |
| Cosmos DB | Standard | €20 |
| AI Search | Basic | €65 |
| **Total** | | **€148-298** |

---

## 🔒 Security Best Practices

### Environment Variables
- ✅ Keep `.env` file local (already in `.gitignore`)
- ✅ Use Azure Key Vault for production secrets (optional)
- ✅ Rotate API keys periodically

### App Service Security
- ✅ HTTPS-only enforced automatically
- ✅ Consider IP restrictions for production
- ✅ Enable Application Insights for monitoring

### Network Security
- ✅ Consider VNet integration for high security
- ✅ Use Private Endpoints for Azure services (enterprise)

---

## 📚 Additional Resources

### Files in deployment/ Directory

- `deploy-with-env.ps1` - **Main deployment script**
- `README.md` - Deployment overview and file descriptions
- `DEPLOYMENT_GUIDE.md` - **This file** - Complete deployment guide

### Documentation References

- [Azure App Service Python](https://docs.microsoft.com/azure/app-service/quickstart-python)
- [Azure OpenAI Service](https://docs.microsoft.com/azure/cognitive-services/openai/)
- [Azure Cosmos DB](https://docs.microsoft.com/azure/cosmos-db/)
- [Azure AI Search](https://docs.microsoft.com/azure/search/)

---

## 🆘 Support

For deployment issues:

1. **Check logs first**: `az webapp log tail`
2. **Verify prerequisites**: Azure services and credentials
3. **Review troubleshooting section above**
4. **Contact**: Andrea Natali @ Avanade

---

**🎉 Success! ALMA is now live on Azure and ready for production use!**
