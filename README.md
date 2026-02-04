# 🎯 ALMA - Advanced Learning & Metadata Assistant

Intelligent chatbot for managing ETL configurations in the Bacardi GDA CPGAI framework.

**Status**: ✅ **Production Ready** - Successfully deployed on Azure App Service

A FastAPI-based chatbot application that assists developers in configuring ETL (Extract, Transform, Load) pipelines using Azure OpenAI and Semantic Kernel. The assistant provides guidance in creating parametric JSON configurations and can query existing configurations stored in Azure Cosmos DB.



---



## 🌟 Key Features

- 🤖 **Advanced AI Assistant**: Powered by Azure OpenAI (GPT-4o) for natural language interactions
- 🔍 **RAG (Retrieval-Augmented Generation)**: Retrieves technical documentation from Azure AI Search
- 💾 **Cosmos DB Integration**: Real-time query and management of ETL configurations
- 🎯 **ALMA Personality**: AI assistant with professional, youthful, and engaging personality traits
- 🚀 **FastAPI Backend**: Modern, high-performance Python framework
- 📊 **Interactive Frontend**: User-friendly web interface with real-time chat
- ⚡ **Production-Ready**: Validated deployment on Azure App Service with complete guide
- 💬 **ETL Configuration Assistant**: Help in creating and configuring parametric JSON files for ETL pipelines
- 🔎 **Advanced Cosmos DB Queries**: Search and retrieve existing configurations with pre-execution validations
- 🔢 **Application-Side Counting**: COUNT functionality despite Cosmos DB limitations
- 📚 **RAG-based Documentation**: Access to complete ETL documentation via Retrieval-Augmented Generation with semantic titles
- ✅ **Pre-Execution Validations**: Input validation prevents invalid operations before execution

---

## 🏗️ Architecture

The application follows a modular architecture based on Semantic Kernel plugins:



### Available Plugins

1. **EtlConfigPlugin**: Technical documentation retrieval via RAG
   - Azure AI Search with semantic ranking
   - Semantic titles for improved relevance
   - Pre-execution validation

2. **CosmosDbPlugin**: Configuration query and management
   - `query_configurations`: SQL-like queries on configurations
   - `count_configurations`: Application-side counting with statistics
   - `list_by_domain`: List configurations by domain
   - `get_schema_info`: Database schema information

3. **TextPlugin**: Text manipulation (built-in Semantic Kernel)

The application consists of:

- **FastAPI Backend**: RESTful API with chat endpoints
- **Semantic Kernel**: Microsoft SDK for LLM orchestration with native functions

| Layer | Technology | Version |
|-------|-----------|---------|
| **Backend** | FastAPI | 0.121.0 |
| **Server** | Uvicorn + Gunicorn | 0.34.0 + 23.0.0 |
| **AI/ML** | Semantic Kernel | 1.38.0 |
| **OpenAI** | openai | 1.109.1+ |
| **Database** | Azure Cosmos DB | SQL API |
| **Search** | Azure AI Search | Standard+ |
| **Deployment** | Azure App Service | Linux, Python 3.11 |

**Custom Plugins:**
- `EtlConfigPlugin`: RAG-based documentation search with Azure AI Search
- `CosmosDbPlugin`: Azure Cosmos DB query capabilities

**Frontend**: HTML/JavaScript interface with Tailwind CSS

**Azure Services**: 
- Azure OpenAI (GPT-4o)
- Azure Cosmos DB (SQL API)
- Azure AI Search (vector store for RAG)

For complete architectural details, see [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.11.x** (required for Azure deployment)
- **Azure CLI** (for deployment)
- **PowerShell** (for deployment scripts)
- **Azure OpenAI service** instance with GPT-4o model deployed
- **Azure Cosmos DB** account (SQL API)
- **Azure AI Search** service (for RAG functionality)
- Azure account with configured resources

### Local Setup (5 minutes)

#### 1. Clone and Virtual Environment

```bash
cd cpgai_chatbot
python -m venv venv-minimal
venv-minimal\Scripts\activate  # Windows
# source venv-minimal/bin/activate  # Linux/Mac
```

#### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

⚠️ **Critical Dependencies**: DO NOT modify without validation
- `semantic-kernel[openai]==1.38.0` → automatically installs `openai>=1.109.1`
- openai version 1.109.1+ is **required** for the `omit` export

#### 3. Configure `.env`

Create a `.env` file in the project root with these variables:

```env
# Azure OpenAI
AZURE_OPENAI_API_KEY=your_key
AZURE_OPENAI_ENDPOINT=https://your-openai.cognitiveservices.azure.com/

AZURE_OPENAI_API_VERSION=2025-01-01-preview
AZURE_OPENAI_CHAT_MODEL_NAME=gpt-4o
AZURE_OPENAI_EMBEDDING_MODEL_NAME=text-embedding-3-small

# Azure Cosmos DB
COSMOS_DB_ENDPOINT=https://your-cosmos.documents.azure.com:443/
COSMOS_DB_KEY=your_key
COSMOS_DB_DATABASE_NAME=metadata
COSMOS_DB_CONTAINER_NAME=configurations

# Azure AI Search
AZURE_AI_SEARCH_ENDPOINT=https://your-search.search.windows.net
AZURE_AI_SEARCH_KEY=your_key
AZURE_AI_SEARCH_INDEX_NAME=cpgai-gda-version

# Application
ENVIRONMENT=development
LOG_LEVEL=INFO
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```



#### 4. Start Local Server

```bash
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

#### 5. Verify Functionality

```bash
# Health check
curl http://127.0.0.1:8000/api/health

# Browser:
# Frontend:        http://127.0.0.1:8000/
# API Docs:        http://127.0.0.1:8000/docs
# Interactive API: http://127.0.0.1:8000/redoc
```

**Expected Health Check Response**:
```json
{
  "status": "healthy",
  "message": "ETL Assistant API is running",
  "kernel_available": true,
  "active_sessions": 0
}
```



---# source venv-minimal/bin/activate  # Linux/Maccp .env.example .env



## 🌐 Azure App Service Deployment``````



### ⚡ Automated Deployment (Recommended)



```powershell
cd deployment

.\deploy-with-env.ps1 -ResourceGroup "Your-Resource-Group" -WebAppName "your-app-name"
```

The script automates:

- ✅ Reading variables from `.env`
- ✅ Configuring Azure App Service settings
- ✅ Creating ZIP with `tar` (POSIX-compatible paths)
- ✅ Asynchronous upload and deployment
- ✅ Deployment status monitoring



### 📚 Complete Deployment Documentation

For detailed guide with comprehensive troubleshooting:

**[📖 DEPLOYMENT_GUIDE_FINAL.md](deployment/DEPLOYMENT_GUIDE_FINAL.md)**



Includes:

- ✅ Prerequisites and configuration

- ✅ Step-by-step deployment (automated + manual)
- ✅ Critical dependency resolution explanation
- ✅ Complete troubleshooting (DISABLE_COLLECTSTATIC, timeout, HTTP 400, openai versions)
- ✅ Monitoring and deployment verification
- ✅ Local testing procedures

- ✅ Pre-deployment checklist

### 🎯 Manual Deployment (Alternative)

If you prefer full control:

```powershell
# 1. Login to Azure CLI
az login

# 2. Create ZIP with tar (POSIX paths)
tar -a -cf deploy.zip app frontend startup.sh runtime.txt requirements-minimal.txt .env



# 3. Deploy
az webapp deploy `
  --resource-group "Your-RG" `
  --name "your-app-name" `
  --src-path deploy.zip `
  --type zip `
  --async true `
  --timeout 600000

# 4. Configure App Settings
az webapp config appsettings set `
  --resource-group "Your-RG" `
  --name "your-app-name" `
  --settings @.env.json

# 5. Verify deployment

az webapp log tail --resource-group "Your-RG" --name "your-app-name"### 4. Setup Azure Resources

```

# Azure AI Search

---

AZURE_AI_SEARCH_ENDPOINT=https://your-search.search.windows.net#### Azure Cosmos DB

## 📦 Project Structure

AZURE_AI_SEARCH_KEY=your_key1. Create a Cosmos DB account with SQL API

```

cpgai_chatbot/AZURE_AI_SEARCH_INDEX_NAME=cpgai-gda-version2. Create a database named `metadata`

├── 📄 README.md                          # ⬅️ This file
├── 📄 requirements-minimal.txt           # Production dependencies (13 packages)
├── 📄 runtime.txt                        # Python version for Azure
├── 📄 .env                               # Configuration (DO NOT commit!)
├── 📄 pytest.ini                         # Test configuration
│

├── 📁 app/                               # 🚀 Main application
│   ├── main.py                          # FastAPI entry point
│   ├── api/                             # API router
│   │   └── router.py                    # REST endpoints (/api/chat, /api/health)
│   ├── core/                            # Core configuration
│   │   ├── config.py                    # Settings management
│   │   └── kernel_factory.py           # Semantic Kernel factory
│   ├── plugins/                         # Semantic Kernel plugins
│   │   ├── EtlConfigPlugin/            # RAG documentation plugin
│   │   └── CosmosDbPlugin/             # Cosmos DB plugin (queries + count)

│   └── services/                        # Business logic
│
├── 📁 frontend/                          # 🌐 Web frontend
│   ├── index.html                       # ALMA homepage
│   └── script.js                        # Chat interface JavaScript
│

├── 📁 deployment/                        # 🚢 Deployment automation
│   ├── deploy-with-env.ps1             # Main deployment script
│   └── DEPLOYMENT_GUIDE_FINAL.md       # Complete deployment guide
│
├── 📁 tests/                             # 🧪 Test suite
│   ├── test_azure_services.py          # Azure integration tests

│   ├── test_cosmos_comprehensive.py    # Cosmos DB tests
│   ├── test_azure_search.py            # Azure AI Search tests
│   ├── test_rag_extended.py            # RAG tests
│   ├── test_count_direct.py            # Application-side counting tests
│   └── test_validations_high_priority.py # Pre-execution validation tests

│# Health check   - `layer` (Edm.String, filterable)

├── 📁 data/                              # 📊 Data processing

│   ├── process_document_optimized.py   # Document processorcurl http://127.0.0.1:8000/api/health   - `process_type` (Edm.String, filterable)

│   ├── reindex_search.py               # Azure AI Search indexing

│   └── examples/                        # JSON configuration examples   - `domain` (Edm.String, filterable)

│

└── 📁 docs/                              # 📖 Documentation# Browser:    - `chunk_index` (Edm.Int32)

    ├── ARCHITECTURE.md                  # Detailed architecture

    ├── TOKEN_MANAGEMENT_SOLUTION.md    # Token management# Frontend:        http://127.0.0.1:8000/   - `keywords` (Collection(Edm.String), searchable)

    └── RECENT_IMPROVEMENTS.md          # Recent improvements changelog

```# API Docs:        http://127.0.0.1:8000/docs3. Configure semantic configuration for ranking



---# Interactive API: http://127.0.0.1:8000/redoc4. Note down the endpoint and admin key



## 💬 Usage Examples```



### Chat Interface### 5. Process Documentation



Open browser at `http://localhost:8000` (local) or `https://your-app.azurewebsites.net` (Azure).**Risposta Attesa Health Check**:



**Example questions**:```json**Important**: Before starting the application, you must process and index the ETL documentation:



```{

✅ "Who are you?"

   → ALMA introduces herself with personality  "status": "healthy",```bash



✅ "How many configurations do we have for NielsenGB?"  "message": "ETL Assistant API is running",# Ensure ETL_Configuration.docx file is in data/

   → Application-side counting with statistics

  "kernel_available": true,# Process the document and generate chunks

✅ "Help me configure a Silver layer transformation with upsert mode"

   → Step-by-step guidance with documentation retrieval  "active_sessions": 0python data/process_document_optimized.py



✅ "Show me an example of Bronze configuration for NielsenUS"}

   → Cosmos DB query + JSON example

```# Index chunks in Azure AI Search

✅ "What parameters are needed for bulk-hash transformation?"

   → RAG search of technical documentationpython data/reindex_search.py



✅ "Give me a complete JSON configuration for a Silver job with upsert"---```

   → Guided configuration generation



✅ "List all configurations for domain NielsenUK"

   → Fuzzy matching suggestion if domain is incorrect## 🌐 Azure App Service DeploymentThis process:

```

- Extracts content from `ETL_Configuration.docx`

### API Usage (cURL)

### ⚡ Automated Deployment (Recommended)- Creates optimized chunks (2000-4000 characters)

```bash

# 1. Chat message- Generates metadata and keywords for each chunk

curl -X POST "https://your-app.azurewebsites.net/api/chat" \

  -H "Content-Type: application/json" \```powershell- Uploads everything to Azure AI Search for RAG queries

  -d '{

    "message": "How to configure upsert mode in Silver layer?",cd deployment

    "session_id": "user123"

  }'.\deploy-with-env.ps1 -ResourceGroup "Your-Resource-Group" -WebAppName "your-app-name"### 6. Start the Application



# 2. Health check```

curl https://your-app.azurewebsites.net/api/health

Using the startup script (recommended):

# 3. Clear session

curl -X POST "https://your-app.azurewebsites.net/api/clear-session" \The script automates:

  -H "Content-Type: application/json" \

  -d '"user123"'- ✅ Reading variables from `.env````bash

```

- ✅ Configuring Azure App Service settings# Make script executable (first time only on Linux/macOS)

---

- ✅ Creating ZIP with `tar` (POSIX-compatible paths)chmod +x startup.sh

## 🧪 Testing

- ✅ Asynchronous upload and deployment

### Complete Test Suite

- ✅ Deployment status monitoring# Start the application

```bash

# From project root./startup.sh

pytest tests/ -v

```### 📚 Complete Deployment Documentation```



### Specific Tests



```bashFor detailed guide with comprehensive troubleshooting:Or manually:

# Test critical imports

python test_imports.py



# Test Azure Search**[📖 DEPLOYMENT_GUIDE_FINAL.md](deployment/DEPLOYMENT_GUIDE_FINAL.md)**```bash

pytest tests/test_azure_search.py -v

# Recommended: Watch only app directory to avoid venv reload issues

# Test Cosmos DB

pytest tests/test_cosmos_comprehensive.py -vInclude:uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload --reload-dir app



# Test RAG- ✅ Prerequisites and configuration

pytest tests/test_rag_extended.py -v

- ✅ Step-by-step deployment (automated + manual)# Alternative: Watch all directories (may cause issues on Windows)

# Test application-side counting

pytest tests/test_count_direct.py -v- ✅ Spiegazione dependency resolution critica# uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload



# Test pre-execution validations- ✅ Troubleshooting completo (DISABLE_COLLECTSTATIC, timeout, HTTP 400, versioni openai)```

pytest tests/test_validations_high_priority.py -v

```- ✅ Monitoring e verifica deployment



### Local Pre-Deployment Validation- ✅ Local testing procedures**Note**: On Windows, using `--reload` without `--reload-dir` may cause continuous reload loops due to WatchFiles monitoring the `venv` directory. Always use `--reload-dir app` to avoid this issue.



Before deploying, validate everything works locally:- ✅ Pre-deployment checklist



```bash### 7. Access the Application

# 1. Activate venv

venv-minimal\Scripts\activate### 🎯 Manual Deployment (Alternative)



# 2. Test importsOpen your browser and navigate to:

python test_imports.py

# Should print: ✅ All imports successfulIf you prefer full control:- **Web Interface**: http://localhost:8000



# 3. Start local server- **API Documentation**: http://localhost:8000/docs

python -m uvicorn app.main:app --host 127.0.0.1 --port 8000

```powershell- **API Health Check**: http://localhost:8000/api/health

# 4. Test health endpoint (different window)

curl http://127.0.0.1:8000/api/health# 1. Login to Azure CLI

```

az login## 💬 Usage Examples

---



## 📊 Main API Endpoints

# 2. Create ZIP with tar (POSIX paths)### Chat Interface

### `GET /api/health`

tar -a -cf deploy.zip app frontend startup.sh runtime.txt requirements-minimal.txt .env

Verify application status and Semantic Kernel availability.

1. Open the web interface at http://localhost:8000

**Response**:

```json# 3. Deploy2. Try these example queries:

{

  "status": "healthy",az webapp deploy `   - "Who are you?" - Meet ALMA!

  "message": "ETL Assistant API is running",

  "kernel_available": true,  --resource-group "Your-RG" `   - "How many configurations do we have for NielsenGB?" - Application-side counting

  "active_sessions": 0

}  --name "your-app-name" `   - "Help me configure a Silver layer transformation with upsert mode"

```

  --src-path deploy.zip `   - "Show me an example of Bronze layer configuration for NielsenUS"

### `POST /api/chat`

  --type zip `   - "What parameters are needed for bulk-hash transformation?"

Interact with ALMA via chat.

  --async true `   - "Give me a complete JSON configuration for a Silver job with upsert"

**Request**:

```json  --timeout 600000   - "List all configurations for domain NielsenUK" - Will suggest correct domain (NielsenUS, NielsenPT, etc.)

{

  "message": "Search Bronze layer configurations for SAPBW domain",

  "session_id": "default"

}# 4. Configure App Settings### API Usage

```

az webapp config appsettings set `

**Response**:

```json  --resource-group "Your-RG" ````bash

{

  "response": "I found 15 Bronze configurations for SAPBW...",  --name "your-app-name" `# Send a chat message

  "session_id": "default",

  "timestamp": "2025-01-17T10:30:00Z"  --settings @.env.jsoncurl -X POST "http://localhost:8000/api/chat" \

}

```  -H "Content-Type: application/json" \



### `POST /api/clear-session`# 5. Verify deployment  -d '{



Clear chat history for session_id.az webapp log tail --resource-group "Your-RG" --name "your-app-name"    "message": "How to configure upsert mode in Silver layer?",



**Request**:```    "session_id": "user123"

```json

"user123"  }'

```

---

**Response**:

```json# Clear chat session

{

  "status": "cleared",## 📦 Project Structurecurl -X POST "http://localhost:8000/api/clear-session" \

  "session_id": "user123"

}  -H "Content-Type: application/json" \

```

```  -d '"user123"'

### `GET /docs`

cpgai_chatbot/

Swagger UI - Interactive API documentation.

├── 📄 README.md                          # ⬅️ Questo file# Check API status

### `GET /redoc`

├── 📄 requirements-minimal.txt           # Dipendenze production (13 packages)curl http://localhost:8000/api/health

ReDoc - Alternative API documentation.

├── 📄 runtime.txt                        # Python version per Azure```

---

├── 📄 .env                               # Configuration (DO NOT commit!)

## 🔧 Advanced Configuration

├── 📄 pytest.ini                         # Test configuration## 📁 Project Structure

### Token Management

│

L'applicazione implementa gestione token per evitare overflow del context window:

├── 📁 app/                               # 🚀 Applicazione principale```

- **Automatic chat history truncation**: Max 10 messages

- **Estimated token limit**: ~100,000 tokens (below GPT-4o's 128k limit)│   ├── main.py                          # Entry point FastAPIcpgai_chatbot/

- **Automatic session reset**: If needed to maintain performance

│   ├── api/                             # Router API├── README.md                         # Main documentation

Dettagli: [TOKEN_MANAGEMENT_SOLUTION.md](docs/TOKEN_MANAGEMENT_SOLUTION.md)

│   │   └── router.py                    # Endpoints REST (/api/chat, /api/health)├── requirements.txt                  # Python dependencies

### Function Calling

│   ├── core/                            # Core configuration├── startup.sh                        # Application startup script

ALMA utilizza function calling automatico tramite Semantic Kernel per:

│   │   ├── config.py                    # Settings management├── pytest.ini                        # Pytest configuration

1. **Retrieve technical documentation** (RAG via Azure AI Search)

2. **Execute SQL queries** on Cosmos DB│   │   └── kernel_factory.py           # Semantic Kernel factory├── .env.example                      # Environment variables template

3. **Count configurations** (application-side counting)

4. **Manipulate text** (built-in Semantic Kernel)│   ├── plugins/                         # Plugin Semantic Kernel├── .gitignore                        # Git ignore rules



Il kernel sceglie automaticamente le funzioni più appropriate in base al messaggio dell'utente.│   │   ├── EtlConfigPlugin/            # RAG documentation plugin│



### CORS Configuration│   │   └── CosmosDbPlugin/             # Cosmos DB plugin (queries + count)├── app/                              # Main application code



Per configurare origini CORS diverse:│   └── services/                        # Business logic│   ├── __init__.py



```env││   ├── main.py                       # FastAPI entry point

# .env

CORS_ORIGINS=https://your-frontend.com,https://another-domain.com├── 📁 frontend/                          # 🌐 Frontend web│   ├── api/                          # API routes and endpoints

```

│   ├── index.html                       # Homepage ALMA│   │   ├── __init__.py

Oppure modifica `app/main.py`:

│   └── script.js                        # Chat interface JavaScript│   │   └── router.py                 # Chat endpoints

```python

app.add_middleware(││   ├── core/                         # Core configuration

    CORSMiddleware,

    allow_origins=["https://specific-domain.com"],├── 📁 deployment/                        # 🚢 Deployment automation│   │   ├── __init__.py

    allow_credentials=True,

    allow_methods=["*"],│   ├── deploy-with-env.ps1             # Script deployment principale│   │   ├── config.py                 # Settings management

    allow_headers=["*"],

)│   └── DEPLOYMENT_GUIDE_FINAL.md       # Guida deployment completa│   │   └── kernel_factory.py        # Semantic Kernel initialization

```

││   ├── plugins/                      # Semantic Kernel plugins

---

├── 📁 tests/                             # 🧪 Test suite│   │   ├── CosmosDbPlugin/           # Azure Cosmos DB integration

## 📝 Note Importanti

│   ├── test_azure_services.py          # Test integrazione Azure│   │   │   ├── __init__.py

### ⚠️ Dipendenze Critiche

│   ├── test_cosmos_comprehensive.py    # Test Cosmos DB│   │   │   └── CosmosDbPlugin.py     # Queries + validations + counting

**NON modificare senza validare**:

│   ├── test_azure_search.py            # Test Azure AI Search│   │   └── EtlConfigPlugin/          # RAG documentation plugin

```txt

semantic-kernel[openai]==1.38.0│   ├── test_rag_extended.py            # Test RAG│   │       ├── __init__.py

```

│   ├── test_count_direct.py            # Test application-side counting│   │       └── EtlConfigPlugin.py    # Semantic search + validations

Questa dipendenza:

- Automatically installs `openai>=1.109.1` via the `[openai]` extra│   └── test_validations_high_priority.py # Test pre-execution validations│   └── services/                     # Business logic

- openai version 1.109.1+ is **required** for the `omit` export from `openai._types`

- Modifying may cause `ImportError: cannot import name 'omit' from 'openai._types'`││       └── __init__.py



**Local validation before deployment**:├── 📁 data/                              # 📊 Data processing│



```bash│   ├── process_document_optimized.py   # Document processor├── frontend/                         # User web interface

python -c "from openai._types import omit; print('✅ omit import OK')"

```│   ├── reindex_search.py               # Azure AI Search indexing│   ├── index.html                    # Main HTML page



### 🔒 Security│   └── examples/                        # JSON configuration examples│   ├── script.js                     # JavaScript for chat interaction



- ✅ `.env` file is in `.gitignore` - **DO NOT commit credentials**││   └── logo.png                      # Application logo

- ✅ Use Azure Key Vault for production (optional but recommended)

- ✅ CORS configured for specific domains (production)└── 📁 docs/                              # 📖 Documentation│

- ✅ Environment variables for all Azure credentials

- ✅ HTTPS mandatory on Azure App Service    ├── ARCHITECTURE.md                  # Detailed architecture├── data/                             # Data processing and sources



### 🚫 Removed Files (Cleanup Completed)    ├── TOKEN_MANAGEMENT_SOLUTION.md    # Gestione token│   ├── ETL_Configuration.docx        # Source documentation



These files were removed as obsolete or unnecessary for production:    └── RECENT_IMPROVEMENTS.md          # Changelog miglioramenti│   ├── process_document_optimized.py # Document processor



- ❌ `requirements.txt`, `requirements-production.txt` (use `requirements-minimal.txt`)```│   ├── reindex_search.py             # Azure AI Search indexing

- ❌ `deploy-azure.ps1`, `deploy-simple.ps1`, etc. (use `deploy-with-env.ps1`)

- ❌ `Dockerfile`, `.dockerignore`, `wheels/` (direct ZIP deployment)│   ├── examples/                     # JSON configuration examples

- ❌ `deploy-logs/`, `deploy-logs-minimal/` (temporary logs)

- ❌ `create_deploy_zip.py`, `test_local_health.py` (temporary scripts)---│   │   ├── AggregatedData-NielsenGB-Bronze-SparklingWine.json



**Only production-ready files maintained**.│   │   ├── CostCenter-SAPBW-Bronze-MDATTR.json



---

## � Usage Examples

### Chat Interface

Open browser at `http://localhost:8000` (local) or `https://your-app.azurewebsites.net` (Azure)

**Example questions:**

✅ "Who are you?"
   → ALMA introduces herself with personality

✅ "How many configurations do we have for NielsenGB?"
   → Application-side counting with statistics

✅ "Help me configure a Silver layer transformation with upsert mode"
   → Step-by-step guide with documentation retrieval

✅ "Show me an example of Bronze layer configuration for NielsenUS"
   → Cosmos DB query + JSON example

✅ "What parameters are needed for bulk-hash transformation?"
   → RAG search of technical documentation

✅ "Give me a complete JSON configuration for a Silver job with upsert"
   → Guided configuration generation

✅ "List all configurations for domain NielsenUK" (typo intentional)
   → Fuzzy matching suggestion for correct domain

### API Usage (cURL)

```bash
# 1. Chat message
curl -X POST "https://your-app.azurewebsites.net/api/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "How to configure upsert mode in Silver layer?",
    "session_id": "user123"
  }'

# 2. Health check
curl https://your-app.azurewebsites.net/api/health

# 3. Clear session
curl -X POST "https://your-app.azurewebsites.net/api/clear-session" \
  -H "Content-Type: application/json" \
  -d '"user123"'
```

---

## 🧪 Testing

### Complete Test Suite

```bash
# From project root
pytest tests/ -v
```

### Specific Tests

```bash
# Test critical imports
python tests/test_imports.py

# Test Azure Search
pytest tests/test_azure_search.py -v

# Test Cosmos DB
pytest tests/test_cosmos_comprehensive.py -v

# Test RAG
pytest tests/test_rag_extended.py -v

# Test application-side counting
pytest tests/test_count_direct.py -v

# Test pre-execution validations
pytest tests/test_validations_high_priority.py -v
```

### Local Pre-Deployment Validation

Before deploying, validate everything works locally:

```bash
# 1. Activate venv
venv-minimal\Scripts\activate

# 2. Test imports
python tests/test_imports.py
# Should print: ✅ All imports successful

# 3. Start local server
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000

# 4. Test health endpoint (different window)
curl http://127.0.0.1:8000/api/health
```

---

## 📊 Main API Endpoints

### `GET /api/health`

Verify application status and Semantic Kernel availability.

**Response**:
```json
{
  "status": "healthy",
  "message": "ETL Assistant API is running",
  "kernel_available": true,
  "active_sessions": 0
}
```

### `POST /api/chat`

Interact with ALMA via chat.

**Request**:
```json
{
  "message": "Search Bronze layer configurations for SAPBW domain",
  "session_id": "default"
}
```

**Response**:
```json
{
  "response": "I found 15 Bronze configurations for SAPBW...",
  "session_id": "default",
  "timestamp": "2025-01-17T10:30:00Z"
}
```

### `POST /api/clear-session`

Clear chat history for session_id.

**Request**:
```json
"user123"
```

**Response**:
```json
{
  "status": "cleared",
  "session_id": "user123"
}
```

### `GET /docs`

Swagger UI - Interactive API documentation.

### `GET /redoc`

ReDoc - Alternative API documentation.

---

## 🔧 Advanced Configuration

```

```

### For other issues

### Environment Variables

Consult the complete guide: [DEPLOYMENT_GUIDE_FINAL.md](deployment/DEPLOYMENT_GUIDE_FINAL.md)

### API Usage (cURL)

---

| Variable | Description | Required | Default |

## 📚 Additional Documentation

```bash|-----------|-------------|-----------|---------|

### Technical Guides

# 1. Chat message| `AZURE_OPENAI_ENDPOINT` | Azure OpenAI service endpoint | ✅ Yes | - |

- **[ARCHITECTURE.md](docs/ARCHITECTURE.md)** - Detailed system architecture

- **[TOKEN_MANAGEMENT_SOLUTION.md](docs/TOKEN_MANAGEMENT_SOLUTION.md)** - Token management strategiescurl -X POST "https://your-app.azurewebsites.net/api/chat" \| `AZURE_OPENAI_API_KEY` | Azure OpenAI API key | ✅ Yes | - |

- **[RECENT_IMPROVEMENTS.md](docs/RECENT_IMPROVEMENTS.md)** - Recent improvements changelog

  -H "Content-Type: application/json" \| `AZURE_OPENAI_CHAT_MODEL_NAME` | Chat model deployment name | ✅ Yes | - |

### Deployment

  -d '{| `AZURE_OPENAI_EMBEDDING_MODEL_NAME` | Embedding model deployment name | ✅ Yes | - |

- **[DEPLOYMENT_GUIDE_FINAL.md](deployment/DEPLOYMENT_GUIDE_FINAL.md)** - Validated complete deployment guide

    "message": "How to configure upsert mode in Silver layer?",| `AZURE_OPENAI_API_VERSION` | Azure OpenAI API version | ✅ Yes | - |

### Testing

    "session_id": "user123"| `COSMOS_DB_ENDPOINT` | Azure Cosmos DB endpoint | ✅ Yes | - |

- **[tests/README.md](tests/README.md)** - Complete testing guide

  }'| `COSMOS_DB_KEY` | Cosmos DB primary key | ✅ Yes | - |

---

| `COSMOS_DB_DATABASE_NAME` | Cosmos DB database name | ✅ Yes | - |

## 🎉 Recent Improvements

# 2. Health check| `COSMOS_DB_CONTAINER_NAME` | Cosmos DB container name | ✅ Yes | - |

### ✅ Production-Ready Deployment (January 2025)

curl https://your-app.azurewebsites.net/api/health| `AZURE_AI_SEARCH_ENDPOINT` | Azure AI Search endpoint | ✅ Yes* | - |

- Resolved dependency conflict (semantic-kernel + openai)

- Implemented automated deployment with `deploy-with-env.ps1`| `AZURE_AI_SEARCH_KEY` | Azure AI Search API key | ✅ Yes* | - |

- Complete local validation pre-deployment

- Optimized Azure App Service configuration# 3. Clear session| `AZURE_AI_SEARCH_INDEX_NAME` | Search index name | ✅ Yes* | - |

- Repository cleanup (removed obsolete files)

- Complete deployment documentationcurl -X POST "https://your-app.azurewebsites.net/api/clear-session" \| `ENVIRONMENT` | Application environment | ❌ No | `development` |



### ✅ Application-Side Counting  -H "Content-Type: application/json" \| `LOG_LEVEL` | Logging level | ❌ No | `INFO` |



Implemented `count_configurations()` to overcome Cosmos DB SQL API limitations:  -d '"user123"'| `CORS_ORIGINS` | Allowed CORS origins | ❌ No | `*` |

- Counting in Python: `len(results)`

- Automatic statistics (domains, layers, markets)```

- Complex filter support

*Required for RAG functionality

### ✅ Pre-Execution Validations

---

Input validations before executing operations:

- Block unsupported aggregations (COUNT, SUM, AVG, GROUP BY)### Cosmos DB Data Model

- Domain validation with fuzzy matching

- Empty search prevention## 🧪 Testing



### ✅ Semantic TitlesThe application expects configuration documents in Cosmos DB with this structure:



Improved search relevance with descriptive titles:### Test Completo

- "Data Ingestion Block (I2_data_ingestion.sink)"

- "ASQL Data Ingestion - Bronze Layer"```json



Details: [RECENT_IMPROVEMENTS.md](docs/RECENT_IMPROVEMENTS.md)```bash{



---# Dalla root del progetto  "id": "unique-configuration-id",



## 👥 Teampytest tests/ -v  "domain": "NielsenUS",



**Bacardi GDA - CPGAI Framework**```  "entity": "AggregatedData",



Developed by: Andrea Natali @ Avanade  "layer": "Bronze",



---### Test Specifici  "process_requested": "ingestion",



## 📄 License  "market": "GB",



Proprietary - Bacardi GDA Project```bash  "partition": ["SparklingWine"],



---# Test importazioni critiche  "dependencyInbound": [],



## 🔗 Useful Linkspython test_imports.py  "dependencyOutbound": ["AggregatedData-Silver"],



### Azure Documentation  "I0_common_conf": {

- [Azure OpenAI Service](https://learn.microsoft.com/azure/ai-services/openai/)

- [Azure Cosmos DB](https://learn.microsoft.com/azure/cosmos-db/)# Test Azure Search    "use-case": "GDF",

- [Azure AI Search](https://learn.microsoft.com/azure/search/)

- [Azure App Service](https://learn.microsoft.com/azure/app-service/)pytest tests/test_azure_search.py -v    "prcs-name": "bronze-process",



### Framework Documentation    "table_name": "AggregatedData"

- [Semantic Kernel](https://learn.microsoft.com/semantic-kernel/)

- [FastAPI](https://fastapi.tiangolo.com/)# Test Cosmos DB  },

- [Uvicorn](https://www.uvicorn.org/)

pytest tests/test_cosmos_comprehensive.py -v  "I1_data_extract_process": {

---

    "type": "data_extract_process",

**Last Updated**: January 17, 2025  

**Version**: 1.0.0  # Test RAG    "sourceList": ["source1"],

**Status**: ✅ **Production Ready** - Successfully Deployed

pytest tests/test_rag_extended.py -v    "source1": {

---

      "type": "asql",

## 🆘 Support

# Test application-side counting      "connection_type": "jdbc",

For support and questions:

pytest tests/test_count_direct.py -v      "source_format": "com.microsoft.sqlserver.jdbc.spark",

1. ✅ Check [DEPLOYMENT_GUIDE_FINAL.md](deployment/DEPLOYMENT_GUIDE_FINAL.md)

2. ✅ Review Troubleshooting section above      "database": "NielsenData",

3. ✅ Check [Azure services status](https://status.azure.com/)

4. ✅ Contact the development team# Test validazioni pre-esecuzione      "schema": "dbo",



---pytest tests/test_validations_high_priority.py -v      "table": "AggregatedData"



**Made with ❤️ for Bacardi GDA by Avanade**```    }


  },

### Validazione Locale Pre-Deployment  "I2_load_data_process": {

    "type": "load_data_process",

Prima di effettuare deployment, validare che tutto funzioni localmente:    "mode-of-write": "append",

    "container": "bronze",

```bash    "target-path": "nielsen/AggregatedData",

# 1. Attiva venv    "target-format": "delta",

venv-minimal\Scripts\activate    "loadType": "full"

  },

# 2. Test imports  "_ts": 1234567890

python test_imports.py}

# Deve stampare: ✅ All imports successful```



# 3. Avvia server locale### Azure AI Search Index Schema

python -m uvicorn app.main:app --host 127.0.0.1 --port 8000

```json

# 4. Test health endpoint (altra finestra){

curl http://127.0.0.1:8000/api/health  "name": "cpgai-gda-version",

```  "fields": [

    {

---      "name": "id",

      "type": "Edm.String",

## 📊 Endpoint API Principali      "key": true,

      "searchable": false

### `GET /api/health`    },

    {

Verify application status and Semantic Kernel availability.      "name": "title",

      "type": "Edm.String",

**Response**:      "searchable": true,

```json      "filterable": false

{    },

  "status": "healthy",    {

  "message": "ETL Assistant API is running",      "name": "content",

  "kernel_available": true,      "type": "Edm.String",

  "active_sessions": 0      "searchable": true,

}      "analyzer": "standard.lucene"

```    },

    {

### `POST /api/chat`      "name": "entity",

      "type": "Edm.String",

Interazione con ALMA tramite chat.      "filterable": true,

      "searchable": true

**Request**:    },

```json    {

{      "name": "layer",

  "message": "Search Bronze layer configurations for SAPBW domain",      "type": "Edm.String",

  "session_id": "default"      "filterable": true,

}      "facetable": true

```    },

    {

**Response**:      "name": "process_type",

```json      "type": "Edm.String",

{      "filterable": true,

  "response": "I found 15 Bronze configurations for SAPBW...",      "facetable": true

  "session_id": "default",    },

  "timestamp": "2025-01-17T10:30:00Z"    {

}      "name": "domain",

```      "type": "Edm.String",

      "filterable": true,

### `POST /api/clear-session`      "facetable": true

    },

Cancella cronologia chat per session_id.    {

      "name": "chunk_index",

**Request**:      "type": "Edm.Int32",

```json      "filterable": true

"user123"    },

```    {

      "name": "keywords",

**Response**:      "type": "Collection(Edm.String)",

```json      "searchable": true

{    }

  "status": "cleared",  ],

  "session_id": "user123"  "semanticConfiguration": {

}    "name": "default",

```    "prioritizedFields": {

      "titleField": {

### `GET /docs`        "fieldName": "title"

      },

Swagger UI - Interactive API documentation.      "contentFields": [

        {

### `GET /redoc`          "fieldName": "content"

        }

ReDoc - Alternative API documentation.      ],

      "keywordsFields": [

---        {

          "fieldName": "keywords"

## 🔧 Advanced Configuration        }

      ]

### Token Management    }

  }

L'applicazione implementa gestione token per evitare overflow del context window:}

```

- **Truncamento automatico chat history**: Max 10 messaggi

- **Limite token stimato**: ~100.000 token (sotto il limite GPT-4o di 128k)**Key Features:**

- **Reset sessione automatico**: Se necessario per mantenere performance- **`title` field**: Semantic titles for improved search relevance (e.g., "Data Ingestion Block (I2_data_ingestion.sink)")

- **Semantic configuration**: Uses `title` as `titleField` for better ranking

Dettagli: [TOKEN_MANAGEMENT_SOLUTION.md](docs/TOKEN_MANAGEMENT_SOLUTION.md)- **Searchable fields**: `content`, `title`, `entity`, `keywords` for comprehensive search



### Function Calling## 🧪 Testing



ALMA utilizza function calling automatico tramite Semantic Kernel per:### Run All Tests



1. **Retrieve technical documentation** (RAG via Azure AI Search)```bash

2. **Execute SQL queries** on Cosmos DB# From project root using pytest

3. **Count configurations** (application-side counting)python -m pytest tests/ -v

4. **Manipulate text** (built-in Semantic Kernel)

# With detailed output

Il kernel sceglie automaticamente le funzioni più appropriate in base al messaggio dell'utente.python -m pytest tests/ -v -s



### CORS Configuration# Specific tests

python -m pytest tests/test_azure_services.py -v

Per configurare origini CORS diverse:```



```env### Run Individual Tests

# .env

CORS_ORIGINS=https://your-frontend.com,https://another-domain.com```bash

```cd tests



Oppure modifica `app/main.py`:# Azure services tests

python test_azure_services.py

```python

app.add_middleware(# Application-side counting tests

    CORSMiddleware,python test_count_direct.py

    allow_origins=["https://specific-domain.com"],

    allow_credentials=True,# Pre-execution validation tests

    allow_methods=["*"],python test_validations_high_priority.py

    allow_headers=["*"],

)# Semantic title ranking tests

```python test_semantic_title_ranking.py



---# Verify indexed documentation

python check_asql_docs.py

## 📝 Note Importanti

# Analyze index content

### ⚠️ Dipendenze Critichepython check_index_content.py

```

**NON modificare senza validare**:

### Key Test Results

```txt

semantic-kernel[openai]==1.38.0**Application-Side Counting** (test_count_direct.py):

```- ✅ NielsenGB: 110 configurations across 5 markets

- ✅ Total: 1750 configurations, 34 unique domains

Questa dipendenza:

- Installa automaticamente `openai>=1.109.1` tramite l'extra `[openai]`**Pre-Execution Validations** (test_validations_high_priority.py):

- openai version 1.109.1+ is **required** for the `omit` export from `openai._types`- ✅ Validation A: Blocks COUNT/SUM/AVG/GROUP BY in queries

- Modifying may cause `ImportError: cannot import name 'omit' from 'openai._types'`- ✅ Validation E: Blocks aggregations in count filter

- ✅ Validation H: Domain validation with fuzzy matching

**Validazione locale prima di deployment**:- ✅ Validation I: Blocks empty search requests



```bashFor more details on testing, see [tests/README.md](tests/README.md).

python -c "from openai._types import omit; print('✅ omit import OK')"

```## 🎉 Recent Improvements



### 🔒 Security

- ✅ `.env` file is in `.gitignore` - **DO NOT commit credentials**
- ✅ Use Azure Key Vault for production (optional but recommended)
- ✅ CORS configured for specific domains (production)
- ✅ Environment variables for all Azure credentials
- ✅ HTTPS mandatory on Azure App Service

### 🚫 Removed Files (Cleanup Completed)**Challenge**: Cosmos DB SQL API doesn't support COUNT(), SUM(), AVG(), GROUP BY.



These files were removed as obsolete or unnecessary for production:**Solution**: Implemented `count_configurations()` function that:

- Retrieves all matching documents with SELECT query

- ❌ `requirements.txt`, `requirements-production.txt` (use `requirements-minimal.txt`)- Counts results in Python: `len(results)`

- ❌ `deploy-azure.ps1`, `deploy-simple.ps1`, etc. (use `deploy-with-env.ps1`)- Automatically extracts statistics (unique domains, layers, markets)

- ❌ `Dockerfile`, `.dockerignore`, `wheels/` (deployment diretto via ZIP)- Returns comprehensive JSON with count + stats + samples

- ❌ `deploy-logs/`, `deploy-logs-minimal/` (log temporanei)

- ❌ `create_deploy_zip.py`, `test_local_health.py` (script temporanei)**Example**:

```python

These files were removed as obsolete or unnecessary for production:.# Question: "How many configs for NielsenGB?"

result = await count_configurations(filter="c.domain = 'NielsenGB'")

---# Returns: {"total_count": 110, "statistics": {...}, "sample_entities": [...]}

```

## 🐛 Troubleshooting

### Pre-Execution Validations

### Issue: `ImportError: cannot import name 'omit' from 'openai._types'`

**Cause**: openai version < 1.109.0 doesn't have the `omit` export required by semantic-kernel.

**Solution**:

```bash
pip uninstall semantic-kernel openai -y
pip install semantic-kernel[openai]==1.38.0
python -c "from openai._types import omit; print('✅ OK')"
```

### Pre-Execution Validations

Input validation **before** database/search operations prevents errors and provides helpful guidance:

1. **Block Unsupported Aggregations**: Prevents COUNT/SUM/AVG/GROUP BY in queries, suggests `count_configurations()`

### Issue: Deployment fails with `DISABLE_COLLECTSTATIC`- **Tables**: "Reference Table - Property"



**Cause**: Wrong value for configuration (used `"1"` instead of `"true"`).All 41 documents reprocessed and reindexed with semantic titles.



**Solution**:## 🔧 Development

```powershell

az webapp config appsettings set `### Development Mode

  --resource-group "Your-RG" `

  --name "your-app-name" ````bash

  --settings DISABLE_COLLECTSTATIC="true"# Install dependencies (if not already done)

```pip install -r requirements.txt



### Issue: Timeout during deployment

**Cause**: Build dependencies requires more than 5 minutes.

**Solution**:

az webapp deploy `

  --src-path deploy.zip `### Adding New Plugins

  --type zip `

  --async true `         # ⬅️ Deployment asincrono1. Create a new directory under `app/plugins/`

  --timeout 600000       # ⬅️ 10 minuti timeout2. Implement the plugin class with `@kernel_function` decorators

```3. Register the plugin in `app/core/kernel_factory.py`



### Issue: HTTP 400 during ZIP upload

**Cause**: Windows path separators (`\`) incompatible with Kudu rsync.

**Solution**: Use `tar` to create ZIP with POSIX paths:

```powershell
tar -a -cf deploy.zip app frontend startup.sh runtime.txt requirements-minimal.txt
```

    

### Issue: Chat history overflow

**Cause**: Too many messages in chat history cause token overflow.

**Solution**: The app automatically handles this by truncating to max 10 messages. If persistent:

```bash
# Clear session via API
curl -X POST "/api/clear-session" -d '"session_id"'
```



### Issue: `ImportError: cannot import name 'omit' from 'openai._types'`Registration in kernel factory:



Consult the complete guide: [DEPLOYMENT_GUIDE_FINAL.md](deployment/DEPLOYMENT_GUIDE_FINAL.md)```python

# app/core/kernel_factory.py

---from app.plugins.MyNewPlugin.MyNewPlugin import MyNewPlugin



## 📚 Additional Documentation# In get_kernel():

kernel.add_plugin(MyNewPlugin(), plugin_name="MyNewPlugin")

### Technical Guides```



- **[ARCHITECTURE.md](docs/ARCHITECTURE.md)** - Detailed system architecture### Debug and Logging

- **[TOKEN_MANAGEMENT_SOLUTION.md](docs/TOKEN_MANAGEMENT_SOLUTION.md)** - Strategie gestione token

- **[RECENT_IMPROVEMENTS.md](docs/RECENT_IMPROVEMENTS.md)** - Changelog miglioramenti recentiThe application uses Python's standard logging. To enable debug logging:



### Deployment```python

# In app/main.py or your module

- **[DEPLOYMENT_GUIDE_FINAL.md](deployment/DEPLOYMENT_GUIDE_FINAL.md)** - Guida deployment validata e completaimport logging

- **[QUICK_START.md](deployment/QUICK_START.md)** - Quick start deployment (se presente)

logging.basicConfig(

### Testing    level=logging.DEBUG,

    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'

- **[tests/README.md](tests/README.md)** - Complete testing guide)

```

---

## 🚀 Deployment

## 🎉 Recent Improvements

### Option 1: Azure Container Instances (Simple)

### ✅ Production-Ready Deployment (January 2025)

```bash

- Risolto dependency conflict (semantic-kernel + openai)# 1. Create a Dockerfile

- Implementato deployment automatico con `deploy-with-env.ps1`cat > Dockerfile << 'EOF'

- Validazione locale completa pre-deploymentFROM python:3.10-slim

- Configurazione Azure App Service ottimizzata

- Cleanup repository (removed obsolete files)WORKDIR /app

- Complete deployment documentation

COPY requirements.txt .

### ✅ Application-Side CountingRUN pip install --no-cache-dir -r requirements.txt



Implemented `count_configurations()` to overcome Cosmos DB SQL API limitations:COPY . .

- Conteggio in Python: `len(results)`

- Statistiche automatiche (domini, layer, market)EXPOSE 8000

- Supporto filtri complessi

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

### ✅ Pre-Execution ValidationsEOF



Input validations before executing operations:# 2. Build Docker image

- Block unsupported aggregations (COUNT, SUM, AVG, GROUP BY)docker build -t etl-assistant-chatbot .

- Domain validation con fuzzy matching

- Empty search prevention# 3. Test locally

docker run -p 8000:8000 --env-file .env etl-assistant-chatbot

### ✅ Semantic Titles

# 4. Push to Azure Container Registry

Improved search relevance with descriptive titles:az acr login --name yourregistry

- "Data Ingestion Block (I2_data_ingestion.sink)"docker tag etl-assistant-chatbot yourregistry.azurecr.io/etl-assistant:latest

- "ASQL Data Ingestion - Bronze Layer"docker push yourregistry.azurecr.io/etl-assistant:latest



Details: [RECENT_IMPROVEMENTS.md](docs/RECENT_IMPROVEMENTS.md)# 5. Deploy to Azure Container Instances

az container create \

---  --resource-group your-rg \

  --name etl-assistant \

## 👥 Team  --image yourregistry.azurecr.io/etl-assistant:latest \

  --cpu 1 --memory 2 \

**Bacardi GDA - CPGAI Framework**  --registry-login-server yourregistry.azurecr.io \

  --registry-username $(az acr credential show -n yourregistry --query username -o tsv) \

Developed by: Andrea Natali @ Avanade  --registry-password $(az acr credential show -n yourregistry --query passwords[0].value -o tsv) \

  --dns-name-label etl-assistant \

---  --ports 8000 \

  --environment-variables \

## 📄 License    AZURE_OPENAI_ENDPOINT=$AZURE_OPENAI_ENDPOINT \

    AZURE_OPENAI_API_KEY=$AZURE_OPENAI_API_KEY \

Proprietary - Bacardi GDA Project    AZURE_OPENAI_CHAT_MODEL_NAME=$AZURE_OPENAI_CHAT_MODEL_NAME \

    COSMOS_DB_ENDPOINT=$COSMOS_DB_ENDPOINT \

---    COSMOS_DB_KEY=$COSMOS_DB_KEY \

    AZURE_AI_SEARCH_ENDPOINT=$AZURE_AI_SEARCH_ENDPOINT \

## 🔗 Useful Links    AZURE_AI_SEARCH_KEY=$AZURE_AI_SEARCH_KEY

```

### Azure Documentation

- [Azure OpenAI Service](https://learn.microsoft.com/azure/ai-services/openai/)### Option 2: Azure App Service (Scalable)

- [Azure Cosmos DB](https://learn.microsoft.com/azure/cosmos-db/)

- [Azure AI Search](https://learn.microsoft.com/azure/search/)```bash

- [Azure App Service](https://learn.microsoft.com/azure/app-service/)# 1. Create App Service Plan

az appservice plan create \

### Framework Documentation  --name etl-assistant-plan \

- [Semantic Kernel](https://learn.microsoft.com/semantic-kernel/)  --resource-group your-rg \

- [FastAPI](https://fastapi.tiangolo.com/)  --sku B1 \

- [Uvicorn](https://www.uvicorn.org/)  --is-linux



---# 2. Create Web App

az webapp create \

**Last Updated**: January 17, 2025    --resource-group your-rg \

**Version**: 1.0.0    --plan etl-assistant-plan \

**Status**: ✅ **Production Ready** - Successfully Deployed  --name etl-assistant-app \

  --runtime "PYTHON:3.10"

---

# 3. Configure Git deployment (or use Azure DevOps)

## 🆘 Supportaz webapp deployment source config \

  --name etl-assistant-app \

For support and questions:  --resource-group your-rg \

  --repo-url https://github.com/your/repo \

1. ✅ Check [DEPLOYMENT_GUIDE_FINAL.md](deployment/DEPLOYMENT_GUIDE_FINAL.md)  --branch main \

2. ✅ Review Troubleshooting section above  --manual-integration

3. ✅ Check [Azure services status](https://status.azure.com/)

4. ✅ Contact the development team# 4. Configure environment variables

az webapp config appsettings set \

---  --resource-group your-rg \

  --name etl-assistant-app \

**Made with ❤️ for Bacardi GDA by Avanade**  --settings \

    AZURE_OPENAI_ENDPOINT=$AZURE_OPENAI_ENDPOINT \
    AZURE_OPENAI_API_KEY=$AZURE_OPENAI_API_KEY \
    # ... other variables

# 5. Configure startup command
az webapp config set \
  --resource-group your-rg \
  --name etl-assistant-app \
  --startup-file "uvicorn app.main:app --host 0.0.0.0 --port 8000"
```

### Option 3: Azure Container Apps (Recommended for production)

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for complete Bicep deployment.

## 🔍 Troubleshooting

### Common Issues

#### 1. Azure OpenAI Connection Errors
```
Error: Azure OpenAI connection failed
```

**Solutions**:
- Verify endpoint URL and API key in `.env`
- Check model deployment names (`AZURE_OPENAI_CHAT_MODEL_NAME`)
- Ensure Azure quotas are not exhausted
- Verify RBAC permissions on Azure OpenAI resource

#### 2. Cosmos DB Connection Issues
```
Error: Unable to connect to Cosmos DB
```

**Solutions**:
- Verify endpoint and key in `.env`
- Check database and container names
- Ensure Cosmos DB firewall allows connections from your IP
- Verify container has partition key `/domain`

#### 3. Missing Environment Variables
```
Error: AZURE_OPENAI_ENDPOINT is not set
```

**Solutions**:
- Copy `.env.example` to `.env`
- Fill in all required Azure credentials
- Verify `.env` is in the project root
- If using Docker, pass variables with `--env-file .env`

#### 4. Empty Azure AI Search Index
```
Warning: No results found in Azure AI Search
```

**Solutions**:
```bash
# Process and reindex documentation
python data/process_document_optimized.py
python data/reindex_search.py

# Verify the index
python tests/check_index_content.py
```

#### 5. Module Import Errors
```
ModuleNotFoundError: No module named 'app'
```

**Solutions**:
```bash
# Ensure you're in the project root
cd cpgai_chatbot

# Activate virtual environment
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

#### 6. Continuous Reload Loop (Windows)
```
WARNING: WatchFiles detected changes in 'venv\...' Reloading...
KeyboardInterrupt
```

**Cause**: WatchFiles monitors the `venv` directory causing infinite reload loops.

**Solutions**:
```bash
# Always use --reload-dir to watch only app directory
uvicorn app.main:app --reload --reload-dir app --host 0.0.0.0 --port 8000

# Alternative: Disable auto-reload for production
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Logs and Debug

#### Enable Detailed Logs

```bash
# Set LOG_LEVEL in .env
LOG_LEVEL=DEBUG

# Or export temporarily
export LOG_LEVEL=DEBUG
uvicorn app.main:app --reload --log-level debug
```

#### Verify Azure Services Status

```bash
# Test connectivity
python tests/test_azure_services.py

# Verify Azure AI Search index
python tests/check_index_content.py

# Complete RAG test
python tests/test_rag_extended.py
```

#### Production Monitoring

For production, configure Application Insights:

```python
# In app/main.py
from opencensus.ext.azure.log_exporter import AzureLogHandler

logger.addHandler(
    AzureLogHandler(
        connection_string='InstrumentationKey=your-key'
    )
)
```

## 📚 Additional Documentation

- **[System Architecture](docs/ARCHITECTURE.md)** - Architectural diagrams and details
- **[Chat Session Management](docs/CHAT_HISTORY_EXPLANATION.md)** - How chat history management works
- **[Token Management](docs/TOKEN_MANAGEMENT_SOLUTION.md)** - Strategies to optimize token usage
- **[Test Guide](tests/README.md)** - Complete testing guide

## 🤝 Contributing

**This repository is public and protected.** The `main` branch cannot be modified directly. All contributions must be made through the fork and pull request workflow.

### Quick Start for Contributors

1. **Fork** the repository to your GitHub account
2. **Clone** your fork locally
3. Create a **feature branch** (`git checkout -b feature/AmazingFeature`)
4. **Commit** your changes (`git commit -m 'feat: add some amazing feature'`)
5. **Push** to your fork (`git push origin feature/AmazingFeature`)
6. Open a **Pull Request** from your fork to this repository

### Important Notes

- ✅ **Fork and PR workflow required** - Direct pushes to `main` are not allowed
- ✅ **Branch protection active** - Ensures code quality and proper review
- ✅ **All contributions welcome** - Through the proper workflow
- 📖 **See [CONTRIBUTING.md](CONTRIBUTING.md)** for complete guidelines

### Contribution Guidelines

- Follow PEP 8 for Python style
- Add tests for new features
- Update documentation
- Ensure all tests pass
- Use conventional commit messages (feat:, fix:, docs:, etc.)

For detailed contribution guidelines, workflow, and best practices, please read **[CONTRIBUTING.md](CONTRIBUTING.md)**.

## 📄 License

This project is released under the MIT License. See `LICENSE` file for details.

## 🆘 Support

For support and questions:
- Open an issue in the repository
- Check the troubleshooting section
- Verify Azure services status
- Contact the development team

## 🔗 Useful Links

- [Azure OpenAI Documentation](https://learn.microsoft.com/azure/ai-services/openai/)
- [Azure Cosmos DB Documentation](https://learn.microsoft.com/azure/cosmos-db/)
- [Azure AI Search Documentation](https://learn.microsoft.com/azure/search/)
- [Semantic Kernel Documentation](https://learn.microsoft.com/semantic-kernel/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)

---

**Version**: 1.0.0  
**Last Updated**: January 2025  
**Maintainer**: Andrea Natali @ Avanade
