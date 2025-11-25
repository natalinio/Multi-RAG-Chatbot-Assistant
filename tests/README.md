# Tests Directory

This folder contains all tests and verification scripts for the ETL chatbot.

## 📋 Test Files

### Azure Services Tests
- **`test_azure_services.py`** - Connectivity tests for Azure OpenAI, Cosmos DB, Azure AI Search
- **`test_azure_search.py`** - Specific tests for Azure AI Search
- **`test_kernel_functions.py`** - Tests for Semantic Kernel functions
- **`test_rag_extended.py`** - Extended tests for RAG (Retrieval Augmented Generation)
- **`test_no_hallucination.py`** - Verify response accuracy and absence of hallucinations
- **`test_reindexed_search.py`** - Tests after reindexing with semantic titles
- **`test_sink_retrieval.py`** - Tests for sink configuration queries

### Advanced Features Tests
- **`test_count_direct.py`** - Application-side counting tests (Cosmos DB limitations workaround)
- **`test_validations_high_priority.py`** - Pre-execution validation tests (HIGH PRIORITY)
- **`test_semantic_title_ranking.py`** - Semantic title ranking tests
- **`test_count_configurations.py`** - Tests for count_configurations() function
- **`test_cosmos_comprehensive.py`** - Comprehensive Cosmos DB plugin tests

### Verification Scripts
- **`check_asql_docs.py`** - Verify ASQL documentation indexed
- **`check_index_content.py`** - Analyze Azure AI Search index content
- **`show_semantic_titles.py`** - Display all generated semantic titles

## 🚀 How to Run Tests

### Prerequisites
```bash
# Make sure the virtual environment is active
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\Activate.ps1  # Windows PowerShell

# Verify all dependencies are installed
pip install -r requirements.txt
```

### Run All Tests with pytest
```bash
# From project root
python -m pytest tests/ -v

# With detailed output
python -m pytest tests/ -v -s

# Specific tests only
python -m pytest tests/test_azure_services.py -v
```

### Run Individual Tests
```bash
cd tests

# Test Azure services
python test_azure_services.py

# Test application-side counting
python test_count_direct.py

# Test pre-execution validations
python test_validations_high_priority.py

# Test semantic title ranking
python test_semantic_title_ranking.py

# Verify ASQL documentation
python check_asql_docs.py

# Analyze index
python check_index_content.py

# Show semantic titles
python show_semantic_titles.py
```

### Quick Test (from root)
```bash
# Runs a quick verification suite
python quick_test.py
```

### HIGH PRIORITY Validations Test
```bash
# Complete tests for all implemented validations
python test_validations_high_priority.py

# Expected output:
# ✅ TEST A: COUNT() blocked in query_existing_config
# ✅ TEST A bis: GROUP BY blocked
# ✅ TEST E: COUNT() blocked in filter
# ✅ TEST H: Invalid domain with suggestions
# ✅ TEST H bis: Valid domain accepted
# ✅ TEST I: Empty search blocked
# ✅ TEST I bis: Whitespace blocked
# 🎉 ALL TESTS PASSED (7/7)
```

## 📊 Test Structure

### Integration Tests
Verify integration with Azure services:
- Azure OpenAI connectivity (GPT-4o)
- Cosmos DB access
- Azure AI Search queries
- RAG plugin functionality

### Content Tests
Verify indexing quality:
- ASQL documentation presence
- Chunk completeness
- Optimal chunk size (2000-4000 chars)
- Complete JSON configurations

### Accuracy Tests
Verify that responses are:
- Based on real data
- Without hallucinations
- Complete and detailed
- Correct according to documentation

### Advanced Features Tests
Verify newly implemented features:
- **Application-Side Counting**: Configuration counting despite Cosmos DB limitations
- **Pre-Execution Validations**: Input validation before execution
  - Block unsupported SQL aggregations
  - Domain validation with fuzzy matching
  - Block empty requests
- **Semantic Titles**: Improved ranking with descriptive semantic titles

## 🔧 Configuration

Tests require the `.env` file to be configured with:
```env
AZURE_OPENAI_ENDPOINT=...
AZURE_OPENAI_API_KEY=...
AZURE_AI_SEARCH_ENDPOINT=...
AZURE_AI_SEARCH_KEY=...
COSMOS_DB_ENDPOINT=...
COSMOS_DB_KEY=...
```

## 📝 Notes

- **Import Path**: Tests use `sys.path.insert(0, ...)` to import modules from root
- **Encoding**: All JSON files are read with `encoding='utf-8'`
- **Async Tests**: Some tests use `asyncio` to test asynchronous functions
- **Exit Codes**: Tests return 0 (success) or 1 (failure)

## 🎯 Expected Results

### ✅ Passed Tests
```
✅ All Tests Passed: 4/4 (100%)

- Repository Structure: OK
- Processed Content: 41 documents with semantic titles
- ASQL Documentation: Found in multiple chunks
- Environment: Configured with all required entries
```

### ✅ Validations Tests (test_validations_high_priority.py)
```
🎉 ALL TESTS PASSED (7/7)

✅ Validation A: COUNT() blocked in query_existing_config
✅ Validation A bis: GROUP BY blocked  
✅ Validation E: COUNT() blocked in filter
✅ Validation H: Invalid domain with suggestions
✅ Validation H bis: Valid domain accepted
✅ Validation I: Empty search blocked
✅ Validation I bis: Whitespace blocked
```

### ✅ Counting Tests (test_count_direct.py)
```
✅ NielsenGB Count: 110 configurations
   - Unique markets: 5 (Config, RTD, SparklingWine, Spirits, Vermouth)

✅ Total Count: 1750 configurations
   - Unique domains: 34
   - Unique layers: 5 (Bronze, Silver, Gold, Interface, Staging)
   - Unique markets: 36
```

### ❌ Common Issues

**ModuleNotFoundError: No module named 'azure.search'**
- Solution: Activate virtual environment and install dependencies

**FileNotFoundError: processed_content.json**
- Solution: Run `python data/process_document_optimized.py`

**KeyError in .env**
- Solution: Copy `.env.example` to `.env` and configure

## 🔗 Links

- [Architecture Documentation](../docs/ARCHITECTURE.md)
- [Token Management](../docs/TOKEN_MANAGEMENT_SOLUTION.md)
- [Recent Improvements](../docs/RECENT_IMPROVEMENTS.md)
