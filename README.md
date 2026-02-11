# 🎯 CORTEX - Cognitive Orchestration & Retrieval Technology EXpert

An intelligent agentic AI system that orchestrates multi-source data retrieval combining semantic search (Azure AI Search) with operational queries (Cosmos DB) for ETL configuration management, powered by Azure OpenAI and Semantic Kernel.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Azure](https://img.shields.io/badge/Azure-OpenAI%20%7C%20Cosmos%20DB%20%7C%20AI%20Search-blue)](https://azure.microsoft.com/)

**Status**: ✅ Production Ready - Successfully Deployed on Azure App Service

---

## 📖 About This Project

### Original Use Case
CORTEX was initially conceived as a **Data Engineering Assistant** to help ETL developers work with a metadata-driven parametric ETL framework:
- **Documentation**: Technical framework documentation indexed in Azure AI Search (PDFs, JSON schemas, guidelines)
- **Operational Data**: ETL job configurations stored as JSON documents in Cosmos DB
- **Target Users**: Data engineers building and managing data pipelines

### 🔄 Adaptability & Reusability

While designed for a specific ETL use case, **CORTEX's architecture is highly adaptable** to any domain or business context requiring:

✅ **Dual Data Access Pattern**:
- **Semantic Search**: Access to indexed documentation (PDFs, Word docs, JSON, technical guides)
- **Operational Queries**: Real-time access to structured data in NoSQL databases

✅ **Common Scenarios**:
- 📚 **Technical Support**: Product documentation + customer tickets/cases
- 🏥 **Healthcare**: Medical guidelines + patient records
- 📦 **Logistics**: Shipping procedures + order tracking data
- 💼 **Finance**: Compliance documentation + transaction records
- 🏭 **Manufacturing**: Process specifications + production data

✅ **Easy Adaptation**:
- Replace Cosmos DB connection with your operational database
- Re-index your domain documentation in Azure AI Search
- Customize Semantic Kernel plugins for your business logic
- Maintain the same agentic orchestration pattern

**The power of CORTEX lies in its ability to intelligently route queries between semantic knowledge retrieval and operational data access**, making it a versatile foundation for enterprise AI assistants across industries.

---

## 🔧 Customization Guide for Domain Adaptation

To adapt CORTEX to your specific domain, you need to customize **three key components**: the Semantic Kernel plugins, the system prompt, and your data sources.

### 1️⃣ **CosmosDbPlugin Configuration** ([app/plugins/CosmosDbPlugin/CosmosDbPlugin.py](app/plugins/CosmosDbPlugin/CosmosDbPlugin.py))

**What to customize:**
- **Document Schema Description**: Update the `@kernel_function` description to reflect your document structure
- **Field Names**: Replace ETL-specific fields (`domain`, `layer`, `entity`, `process_requested`) with your domain fields
- **Known Values**: Update `KNOWN_DOMAINS` list with your valid domain/category values

**Example modifications:**
```python
# Current ETL Schema:
- c.domain: Domain identifier (NielsenUS, SAPBW, Profisee)
- c.layer: Data layer (Bronze, Silver, Gold)
- c.entity: Entity/job name

# Healthcare Example:
- c.department: Department identifier (Cardiology, Oncology, Emergency)
- c.record_type: Record type (Patient, Treatment, Diagnostic)
- c.patient_id: Patient identifier

# E-commerce Example:
- c.category: Product category (Electronics, Clothing, Food)
- c.order_status: Order status (Pending, Shipped, Delivered)
- c.customer_id: Customer identifier
```

**Files to update:**
- Function descriptions in `@kernel_function` decorators
- Validation lists (e.g., `KNOWN_DOMAINS`)
- Example queries in function documentation

### 2️⃣ **EtlConfigPlugin for RAG** ([app/plugins/EtlConfigPlugin/EtlConfigPlugin.py](app/plugins/EtlConfigPlugin/EtlConfigPlugin.py))

**What to customize:**
- **Azure AI Search Index**: Re-index with your domain documentation (PDFs, Word docs, JSON schemas)
- **Function Description**: Update `@kernel_function` description to reflect your documentation content
- **Search Context**: Modify the plugin name and description to match your domain

**Example modifications:**
```python
# Current ETL:
description="Search ETL documentation for configuration guidance, examples, and best practices."

# Healthcare:
description="Search medical guidelines, treatment protocols, and patient care documentation."

# E-commerce:
description="Search product catalogs, shipping procedures, and order fulfillment documentation."
```

**Steps to re-index:**
1. Collect your domain documentation (PDFs, Word, JSON, technical guides)
2. Use Azure AI Search SDK to chunk and index documents
3. Update `azure_ai_search_index_name` in configuration
4. Test semantic search with domain-specific queries

### 3️⃣ **System Prompt Customization** ([app/api/router.py](app/api/router.py))

**What to customize:**
- **Assistant Name & Identity**: Replace "ALMA" references with "CORTEX" or your custom name
- **Domain-Specific Language**: Replace ETL terminology (Bronze/Silver/Gold layers, transformations)
- **Capabilities Description**: Update to reflect your domain operations
- **Example Queries**: Provide domain-relevant examples

**Example customization:**
```python
# Current ETL System Prompt:
"""🎯 Hi! I'm **CORTEX**, your intelligent CPGAI framework assistant!
- **ETL Configurations**: Bronze, Silver, Gold layers
- **Cosmos DB Queries**: Search existing configurations
"""

# Healthcare Example:
"""🎯 Hi! I'm **CORTEX**, your intelligent Healthcare Information assistant!
- **Patient Records**: Search and retrieve patient data
- **Medical Guidelines**: Access treatment protocols and procedures
- **Compliance**: Verify HIPAA-compliant operations
"""

# E-commerce Example:
"""🎯 Hi! I'm **CORTEX**, your intelligent E-commerce Operations assistant!
- **Order Management**: Track and manage customer orders
- **Inventory**: Search product catalogs and stock levels
- **Customer Support**: Access shipping and fulfillment documentation
"""
```

### 4️⃣ **Cosmos DB Connection** ([app/services/cosmos_service.py](app/services/cosmos_service.py))

**What to customize:**
- **Database Name**: Update `cosmos_db_database_name` in `.env`
- **Container Name**: Update `cosmos_db_container_name` with your operational data container
- **Connection String**: Point to your Cosmos DB account

**Environment variables:**
```bash
# .env file
COSMOS_DB_ENDPOINT=https://your-cosmosdb.documents.azure.com:443/
COSMOS_DB_KEY=your-cosmos-key
COSMOS_DB_DATABASE_NAME=your-database-name
COSMOS_DB_CONTAINER_NAME=your-container-name
```

### 5️⃣ **Quick Adaptation Checklist**

- [ ] **Cosmos Schema**: Update field names and descriptions in `CosmosDbPlugin.py`
- [ ] **Known Values**: Replace domain-specific lists (e.g., `KNOWN_DOMAINS`)
- [ ] **Azure AI Search**: Re-index with your domain documentation
- [ ] **System Prompt**: Customize assistant identity and capabilities in `router.py`
- [ ] **Example Queries**: Update usage examples in function descriptions
- [ ] **Environment Variables**: Configure connections to your Azure resources
- [ ] **Testing**: Create domain-specific test queries
- [ ] **README**: Update documentation with your use case

### 📋 Estimated Adaptation Time

- **Basic Adaptation** (schema + prompt): 2-4 hours
- **Full Customization** (re-indexing + testing): 1-2 days
- **Production Deployment**: 3-5 days (including testing and validation)

---

## 🌟 Key Features

- 🤖 **Agentic AI Orchestration**: Powered by Semantic Kernel for intelligent multi-agent coordination
- 🔍 **Dual-Source RAG**: Combines semantic search (Azure AI Search) with structured queries (Cosmos DB)
- 💾 **Unified Data Access**: Real-time retrieval from vector stores and operational databases
- 🎯 **CORTEX Intelligence**: Cognitive orchestration that routes queries to optimal data sources
- 🚀 **FastAPI Backend**: Modern, high-performance Python framework
- 📊 **Interactive Frontend**: User-friendly web interface with real-time chat
- ⚡ **Production-Ready**: Validated deployment on Azure App Service
- 💬 **Configuration Assistant**: Help creating and managing parametric JSON configurations
- 🔎 **Advanced Queries**: Search and retrieve configurations with pre-execution validations
- 🔢 **Smart Counting**: Application-side counting despite Cosmos DB SQL API limitations
- ✅ **Input Validations**: Prevents invalid operations before execution

---

## 🏗️ Architecture

The application follows a modular architecture based on Semantic Kernel plugins:

- **FastAPI Backend**: RESTful API with chat endpoints
- **Semantic Kernel**: Microsoft SDK for LLM orchestration
- **Custom Plugins**:
  - `EtlConfigPlugin`: RAG-based documentation search
  - `CosmosDbPlugin`: Azure Cosmos DB query capabilities
- **Frontend**: HTML/JavaScript interface with Tailwind CSS
- **Azure Services**:
  - Azure OpenAI (GPT Class, you can use whatever model you want provided in AI foundry)
  - Azure Cosmos DB (SQL API)
  - Azure AI Search (vector store for RAG)

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11.x (required for Azure deployment)
- Azure CLI (for deployment)
- Azure OpenAI service with GPT-4o model
- Azure Cosmos DB account (SQL API)
- Azure AI Search service

### Local Setup (5 minutes)

```bash
# 1. Clone repository
git clone https://github.com/natalinio/Multi-RAG-Chatbot-Assistant.git
cd Multi-RAG-Chatbot-Assistant

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate   # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env with your Azure credentials

# 5. Start server
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload

# 6. Open browser
# http://127.0.0.1:8000
```

---

## 💬 Usage Examples

### Chat Interface

Open browser at `http://localhost:8000` and try:

- ✅ "Who are you?" - Meet CORTEX
- ✅ "How many configurations do we have for domain X?" - Cosmos DB query
- ✅ "Help me configure a Silver layer transformation" - Semantic search
- ✅ "Show me an example of Bronze layer configuration" - RAG retrieval
- ✅ "What parameters are needed for bulk-hash transformation?" - Documentation search

### API Usage

```bash
# Chat message
curl -X POST "http://localhost:8000/api/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "How to configure upsert mode?",
    "session_id": "user123"
  }'

# Health check
curl http://localhost:8000/api/health

# Clear session
curl -X POST "http://localhost:8000/api/clear-session" \
  -H "Content-Type: application/json" \
  -d '"user123"'
```

---

## 📊 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/health` | GET | Health check |
| `/api/chat` | POST | Chat with CORTEX |
| `/api/clear-session` | POST | Clear chat history |
| `/docs` | GET | Swagger UI |
| `/redoc` | GET | ReDoc documentation |

---

## 🌐 Azure Deployment

### Automated Deployment

```powershell
cd deployment
.\deploy-with-env.ps1 -ResourceGroup "Your-RG" -WebAppName "your-app-name"
```

For complete deployment guide: [DEPLOYMENT_GUIDE.md](deployment/DEPLOYMENT_GUIDE.md)

---

## 🧪 Testing

```bash
# Run all tests
pytest tests/ -v

# Specific tests
pytest tests/test_azure_search.py -v
pytest tests/test_cosmos_comprehensive.py -v
pytest tests/test_rag_extended.py -v
```

---

## 📚 Documentation

- **[Architecture](docs/ARCHITECTURE.md)** - System architecture details
- **[Deployment Guide](deployment/DEPLOYMENT_GUIDE.md)** - Complete deployment instructions
- **[Testing Guide](tests/README.md)** - Testing procedures
- **[Contributing](CONTRIBUTING.md)** - Contribution guidelines
- **[Security Notice](SECURITY_NOTICE.md)** - Repository sanitization and security information
- **[Repository Protection](REPOSITORY_PROTECTION_IMPLEMENTATION.md)** - Branch protection setup
- **[GitHub Settings Verification](GITHUB_SETTINGS_VERIFICATION.md)** - Settings checklist

---

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'feat: add amazing feature'`)
4. Push to fork (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 🔒 Security

This repository has been sanitized for public use:
- ✅ No actual credentials or API keys
- ✅ No client-specific information
- ✅ Example configurations with placeholder values
- ✅ Comprehensive .gitignore for sensitive files

See [SECURITY_NOTICE.md](SECURITY_NOTICE.md) for details on security measures and sanitization.

**⚠️ Important**: Never commit real credentials. Always use environment variables and keep `.env` files local.

---

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.

---

## 🆘 Support

- Open an issue for bugs or feature requests
- Check [troubleshooting guide](README.md#-troubleshooting)
- Review [documentation](docs/)

---

## 🔗 Useful Links

- [Azure OpenAI Documentation](https://learn.microsoft.com/azure/ai-services/openai/)
- [Semantic Kernel Documentation](https://learn.microsoft.com/semantic-kernel/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Azure Cosmos DB Documentation](https://learn.microsoft.com/azure/cosmos-db/)

---

**Version**: 2.0.0 - CORTEX  
**Last Updated**: February 2026  
**Maintained by**: Development Team