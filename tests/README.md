# Tests Directory

This directory contains test files for CORTEX. Test files are separated into **public** (generic patterns) and **private** (client-specific) categories for security.

---

## 📂 Test File Structure

### ✅ **Public Tests** (Committed to GitHub)

Generic test patterns demonstrating Azure integration:

- **`test_azure_services.py`** - Tests connectivity to Azure OpenAI, Cosmos DB, and Azure AI Search
- **`test_azure_search.py`** - Azure AI Search functionality tests
- **`test_local_health.py`** - Health endpoint verification
- **`test_imports.py`** - Python dependency verification

### ⚠️ **Private Tests** (Local Only - Not Committed)

Tests containing client-specific domain names and configurations:

- `test_cosmos_comprehensive.py`
- `test_validations_high_priority.py`
- `test_token_management.py`
- `test_semantic_title_ranking.py`
- `test_kernel_functions.py`
- `test_no_hallucination.py`
- `test_reindexed_search.py`
- `test_sink_retrieval.py`
- `test_rag_extended.py`
- `test_count_*.py`
- `check_*.py`
- `show_semantic_titles.py`
- `test_asql_integration.py`

These files remain in your local workspace but are excluded from Git via `.gitignore`.

---

## 🚀 Running Tests

### Prerequisites

```powershell
# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Configure environment variables (copy .env.example to .env and fill in your Azure credentials)
```

### Run Public Tests

```powershell
# Test Azure services connectivity
python tests/test_azure_services.py

# Test Azure AI Search
python tests/test_azure_search.py

# Test health endpoint (requires app running)
python tests/test_local_health.py

# Test imports
python tests/test_imports.py
```

### Run All Tests (Local Development)

```powershell
# Run all tests including private ones
pytest tests/ -v

# Run specific test
pytest tests/test_azure_services.py -v
```

---

## 🔐 Security Considerations

### Environment Variables

**All tests use environment variables from `.env` file - never hardcode credentials.**

**Example:**
```python
import os
from dotenv import load_dotenv

load_dotenv()

endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
api_key = os.getenv("AZURE_OPENAI_API_KEY")
```

### Configuration Template

Use `.env.example` as a template:

```bash
cp tests/.env.example .env
# Edit .env with your actual credentials
```

**Required variables:** `AZURE_OPENAI_API_KEY`, `AZURE_OPENAI_ENDPOINT`, `COSMOS_DB_ENDPOINT`, `COSMOS_DB_KEY`, `AZURE_AI_SEARCH_ENDPOINT`, `AZURE_AI_SEARCH_KEY`

### Adding New Tests

**For public tests** (safe to commit):
- Use generic placeholder names
- Load all credentials from environment variables
- No client-specific domain references

**For private tests** (local only):
- Can use real domain names for accurate testing
- Automatically excluded via `.gitignore` patterns

---

## 📊 Test Categories

| Category | Public | Private | Total |
|----------|--------|---------|-------|
| Azure Integration | 2 | 0 | 2 |
| Health & Imports | 2 | 0 | 2 |
| RAG & Search | 0 | 5 | 5 |
| Cosmos DB | 0 | 3 | 3 |
| Validation | 0 | 2 | 2 |
| Utilities | 0 | 3 | 3 |
| **Total** | **4** | **13** | **17** |

---

## 📝 Test Output Examples

### Successful Azure Services Test
```
============================================================
Testing Azure OpenAI Connection
============================================================
Endpoint: https://your-resource.openai.azure.com/
API Version: 2024-12-01-preview
Model Name: gpt-4o

Testing chat completion...
✅ Azure OpenAI: SUCCESS

============================================================
Testing Azure Cosmos DB Connection
============================================================
Endpoint: https://your-cosmos.documents.azure.com:443/
Database: metadata
Container: configurations

✅ Cosmos DB: SUCCESS (Connected to metadata/configurations)

============================================================
Testing Azure AI Search Connection
============================================================
Endpoint: https://your-search.search.windows.net
Index: your-index-name

✅ Azure AI Search: SUCCESS (Index contains 150 documents)
```

---

## 🆘 Troubleshooting

### Missing Dependencies
```powershell
pip install -r requirements.txt
```

### Environment Variables Not Loaded
```powershell
# Verify .env file exists
Test-Path .env

# Check environment variables
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print(os.getenv('AZURE_OPENAI_ENDPOINT'))"
```

### Connection Errors
1. Verify credentials in `.env` file
2. Check Azure resource endpoints are correct
3. Ensure firewall rules allow your IP
4. Verify API keys haven't expired

---

## 📚 Related Documentation

- [Azure OpenAI Documentation](https://learn.microsoft.com/azure/ai-services/openai/)
- [Cosmos DB Best Practices](https://learn.microsoft.com/azure/cosmos-db/)
- [Azure AI Search Documentation](https://learn.microsoft.com/azure/search/)
- [Main README](../README.md)

---

**Note:** Private test files are kept locally for development but automatically excluded from Git commits for security. See `.gitignore` for the complete list of excluded patterns.
