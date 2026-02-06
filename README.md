# 🎯 ALMA - Advanced Learning & Metadata Assistant

An intelligent AI-powered assistant for managing ETL (Extract, Transform, Load) configurations using Azure OpenAI and Semantic Kernel.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Azure](https://img.shields.io/badge/Azure-OpenAI%20%7C%20Cosmos%20DB%20%7C%20AI%20Search-blue)](https://azure.microsoft.com/)

**Status**: ✅ Production Ready - Successfully Deployed on Azure App Service

---

## 🌟 Key Features

- 🤖 **Advanced AI Assistant**: Powered by Azure OpenAI (GPT class) for natural language interactions
- 🔍 **RAG (Retrieval-Augmented Generation)**: Retrieves technical documentation from Azure AI Search
- 💾 **Cosmos DB Integration**: Real-time query and management of ETL configurations
- 🎯 **ALMA Personality**: Professional, engaging AI assistant with specialized ETL knowledge
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
git clone https://github.com/your-org/cpgai_chatbot.git
cd cpgai_chatbot

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

- ✅ "Who are you?" - Meet ALMA
- ✅ "How many configurations do we have for domain X?"
- ✅ "Help me configure a Silver layer transformation"
- ✅ "Show me an example of Bronze layer configuration"
- ✅ "What parameters are needed for bulk-hash transformation?"

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
| `/api/chat` | POST | Chat with ALMA |
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

---

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'feat: add amazing feature'`)
4. Push to fork (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

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

**Version**: 1.0.0  
**Last Updated**: January 2025  
**Maintained by**: Development Team