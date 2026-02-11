# Security Notice - Repository Sanitization

## Overview

This repository has been sanitized to remove client-specific information and sensitive data before being made public on GitHub.

## Actions Taken

### 1. Client Information Removed
All references to specific client names have been replaced with generic terms:
- HTML files (frontend/index.html, app/static/index.html)
- Application code (app/api/router.py)
- Plugin documentation (app/plugins/CosmosDbPlugin/CosmosDbPlugin.py)
- Example data files (data/examples/)
- Documentation files (docs/, deployment/)

### 2. Sensitive Credentials Sanitized
- **Salesforce Configuration**: Replaced actual Salesforce sandbox URLs and client IDs with placeholder values
- **Example Data**: Sanitized table names and file names containing client-specific information
- **.env File**: Properly excluded via .gitignore (only .env.example is committed)

### 3. Build Artifacts Removed
- **venv-minimal directory**: Removed 28 files that should not have been committed
- **Updated .gitignore**: Added venv-minimal/ to prevent future commits

### 4. Data Directory Protected (⚠️ CRITICAL)
**February 2026 Update - CORTEX Rebranding**:
- **Entire `data/` directory excluded** from Git (except README and sanitized examples)
- **Client-specific configurations removed**: 18 JSON files with real ETL configurations
- **Credentials sanitized**: Environment files with database connection strings removed
- **Proprietary documentation excluded**: Technical handbooks and guides not committed
- **Generic templates created**: `data/examples-sanitized/` with anonymized templates

**What was excluded:**
- `data/examples/` - 18 real client configuration files (Nielsen, SAPBW, Profisee, Salesforce)
- `data/processed/` - Processed content chunks indexed in Azure AI Search
- `data/archived/` - Legacy processing scripts
- `*.docx` files - Proprietary technical documentation (ASQL_JsonTemplate_handbook.docx, ETL_Configuration.docx)

**What was included:**
- `data/README.md` - Instructions for data preparation and security best practices
- `data/examples-sanitized/` - 4 generic configuration templates (Bronze/Silver/Gold layers + Environment)
- Processing scripts - `process_document_optimized.py` and `reindex_search.py` (no sensitive data)

### 5. Repository Protection Settings
The repository includes comprehensive branch protection configuration:
- See `REPOSITORY_PROTECTION_IMPLEMENTATION.md` for full details
- Configuration files in `.github/` directory
- Manual setup guide available in `.github/BRANCH_PROTECTION_SETUP.md`

## What Remains in the Repository

### Safe Content
- ✅ Generic application code and architecture
- ✅ Example configuration files with sanitized data
- ✅ Documentation and setup guides
- ✅ Public dependencies and requirements
- ✅ Open-source licensing (MIT License)

### Excluded Content (via .gitignore)
- ❌ Real credentials (.env files)
- ❌ Virtual environments (venv/, venv-minimal/)
- ❌ **Entire data/ directory** (client-specific configurations and documentation)
  - ✅ Exception: data/README.md and data/examples-sanitized/ are included
- ❌ Local data files (*.xlsx, *.csv, *.docx)
- ❌ Azure deployment credentials
- ❌ Logs and temporary files
- ❌ Processed content (data/processed/, data/temp/)

### Sanitized Examples Included
- ✅ `data/examples-sanitized/` - Generic configuration templates
  - Bronze layer ingestion template
  - Silver layer transformation template
  - Gold layer analytics template
  - Environment configuration template
- ✅ All templates use placeholder values (DomainA, DomainB, GenericSourceSystem)
- ✅ No real client names, connection strings, or proprietary logic

## Best Practices for Contributors

### DO NOT Commit:
1. **Actual credentials**: API keys, passwords, connection strings
2. **Client-specific data**: Real data files, customer information, proprietary configurations
3. **Build artifacts**: Virtual environments, compiled files
4. **Local configurations**: Personal .env files, IDE settings
5. **Real documentation**: Client-specific handbooks, technical guides with proprietary info
6. **Data folder content**: Anything in `data/examples/`, `data/processed/`, `data/archived/`
7. **Connection strings**: Even masked or templated ones in environment files

### DO Commit:
1. **Generic code**: Application logic, utilities, helpers
2. **Sanitized examples**: Generic templates in `data/examples-sanitized/`
3. **Documentation**: Setup guides, architecture docs, README files
4. **Public configuration**: .env.example, requirements.txt
5. **Scripts**: Processing and utility scripts without embedded credentials

### Data Directory Guidelines

**When working with domain-specific data:**

✅ **Correct Approach:**
```bash
# Add your real data to excluded directory
cp my-real-config.json data/examples/  # ← Excluded by .gitignore

# Work with the data locally
python data/process_document_optimized.py

# Only commit sanitized examples
cp my-generic-template.json data/examples-sanitized/  # ← Included in Git
```

❌ **NEVER DO THIS:**
```bash
# DON'T: Add real data to tracked directories
cp client-config.json data/examples-sanitized/  # ← Would expose client data!

# DON'T: Modify .gitignore to include data/examples/
# This would expose all client configurations
```

## Verification

### Credentials Check
```bash
# No actual .env file should be present
ls -la | grep "\.env$"  # Should return nothing

# Only .env.example should exist
ls -la | grep ".env.example"  # Should show the example file
```

### Data Directory Check
```bash
# Verify data/ directory is excluded (except allowed files)
git status data/

# Should show:
# - data/README.md (tracked)
# - data/examples-sanitized/ (tracked)
# - Everything else untracked/ignored

# Verify no sensitive files are staged
git diff --cached --name-only | grep "data/examples/"  # Should return nothing
git diff --cached --name-only | grep "data/processed/"  # Should return nothing
```

### Client Name Check
```bash
# No client-specific names should appear in tracked files
grep -r -i "nielsen\|profisee\|sapbw\|salesforce" --exclude-dir=.git --exclude-dir=venv* --exclude-dir=data

# Should only match in:
# - Documentation explaining the USE CASE (acceptable)
# - NOT in actual code or configuration files
```

### Connection String Check
```bash
# No real connection strings
grep -r "database.windows.net" --exclude-dir=.git --exclude-dir=venv* --exclude-dir=data

# Should only appear in:
# - data/examples-sanitized/ with placeholder values
# - .env.example with placeholder values
```

## Security Contacts

If you discover sensitive information that was missed in the sanitization:
1. **DO NOT** create a public issue
2. Contact the repository maintainer directly
3. Report through GitHub Security Advisory if available

## Compliance

This repository follows:
- **MIT License**: Open-source licensing
- **No Personal Data**: No PII or customer data
- **No Secrets**: All credentials excluded
- **Generic Examples**: Only sanitized sample data

## Audit Trail

### Sanitization Date
- **Date**: February 6, 2025
- **Commit**: Remove venv-minimal and sanitize Bacardi references
- **Branch**: copilot/vscode-mlasypjy-9os9

### Files Modified
- 10+ files with client references sanitized
- 28 venv files removed from tracking
- .gitignore updated

### Verification Status
- ✅ No actual credentials in repository
- ✅ No client-specific names in public files
- ✅ No build artifacts committed
- ✅ Proper .gitignore configuration
- ✅ Branch protection guidelines provided

---

**Last Updated**: February 2025  
**Status**: Repository Sanitized and Ready for Public Use
