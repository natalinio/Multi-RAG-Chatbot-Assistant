# Test Directory Structure

This directory contains test files for the CORTEX chatbot application. Due to security considerations, test files are categorized as follows:

## 📂 Public Test Files (Committed to GitHub)

These files contain generic testing patterns and can be safely shared:

### Azure Service Integration Tests
- **`test_azure_services.py`** ✅
  - Tests connectivity to Azure OpenAI, Cosmos DB, and Azure AI Search
  - Uses environment variables exclusively (no hardcoded credentials)
  - Demonstrates proper Azure service integration patterns

### Basic Health & Import Tests  
- **`test_local_health.py`** ✅
  - Health endpoint verification
  - Generic application status checks

- **`test_imports.py`** ✅
  - Python dependency verification
  - Import integrity checks

### Configuration Templates
- **`.env.example`** ✅
  - Template for environment variables
  - Shows required configuration without exposing real credentials

### Documentation
- **`README.md`** ✅
  - Testing guide and documentation
  - How to run tests and interpret results

- **`SECURITY_ANALYSIS.md`** ✅
  - Security audit of test files
  - Classification of safe vs. sensitive content

## 🔒 Private Test Files (Local Only - Not Committed)

These files contain client-specific domain names, system references, or configuration examples:

### Client-Specific Tests (Excluded via .gitignore)
- `test_validations_high_priority.py` ⚠️ - References: NielsenGB, NielsenUK
- `test_token_management.py` ⚠️ - References: NielsenGB domain
- `test_semantic_title_ranking.py` ⚠️ - References: Profisee, SFAsseco
- `test_cosmos_comprehensive.py` ⚠️ - May contain client query patterns
- `test_kernel_functions.py` ⚠️ - References: SAPBW, sapcdc
- `test_no_hallucination.py` ⚠️ - References: SAPBW configurations
- `test_reindexed_search.py` ⚠️ - References: SAPBW ingestion
- `test_sink_retrieval.py` ⚠️ - Client-specific configuration names
- `test_rag_extended.py` ⚠️ - Client-specific queries
- `test_count_*.py` ⚠️ - Client-specific counting logic
- `check_*.py` ⚠️ - Verification scripts with client data

## 🚀 Running Tests

### Prerequisites
```powershell
# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp tests/.env.example .env
# Edit .env with your actual Azure credentials
```

### Run Public Tests
```powershell
# Azure services connectivity
python tests/test_azure_services.py

# Health check
python tests/test_local_health.py

# Import verification
python tests/test_imports.py
```

### Run All Tests (Local Development Only)
```powershell
pytest tests/ -v
```

## 🔐 Security Considerations

### ✅ Safe Practices Implemented:
1. **No hardcoded credentials** - All tests use `os.getenv()` and `load_dotenv()`
2. **`.env` is gitignored** - Real credentials never committed
3. **Client-specific tests excluded** - Domain names and system references kept private
4. **Template provided** - `.env.example` shows required structure without exposing data

### ⚠️ Before Committing New Tests:
1. Check for client-specific domain names (Nielsen, SAPBW, Profisee, etc.)
2. Verify no hardcoded endpoints or credentials
3. Use generic placeholder names for examples
4. Add to `.gitignore` if test contains sensitive references

## 📝 Adding New Tests

For **generic tests** (safe for public GitHub):
```python
import os
from dotenv import load_dotenv

load_dotenv()

# Use environment variables
endpoint = os.getenv("AZURE_SERVICE_ENDPOINT")
api_key = os.getenv("AZURE_SERVICE_KEY")

# Use generic placeholder names in examples
example_domain = "SourceSystemA"
example_config = "DataIngestion-SystemA-Bronze-Template"
```

For **client-specific tests** (local only):
1. Use real domain names as needed for accurate testing
2. Add filename pattern to `.gitignore` if not already covered
3. Document in `SECURITY_ANALYSIS.md`

## 🎯 Test Coverage

| Category | Public Tests | Private Tests | Total |
|----------|--------------|---------------|-------|
| Azure Integration | ✅ 1 | ⚠️ 0 | 1 |
| Health & Imports | ✅ 2 | ⚠️ 0 | 2 |
| RAG & Search | ✅ 0 | ⚠️ 5 | 5 |
| Cosmos DB | ✅ 0 | ⚠️ 3 | 3 |
| Validation | ✅ 0 | ⚠️ 2 | 2 |
| Utilities | ✅ 0 | ⚠️ 2 | 2 |
| **Total** | **3** | **12** | **15** |

## 📚 Further Reading

- [Azure OpenAI Service Documentation](https://learn.microsoft.com/azure/ai-services/openai/)
- [Cosmos DB Best Practices](https://learn.microsoft.com/azure/cosmos-db/)
- [Azure AI Search Documentation](https://learn.microsoft.com/azure/search/)
