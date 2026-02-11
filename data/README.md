# Data Directory

⚠️ **This directory is excluded from Git for security reasons** (see `.gitignore`).

## Purpose

This directory contains domain-specific data used by CORTEX for:
- **Documentation indexing**: Technical guides, JSON schemas, configuration handbooks
- **Example configurations**: Sample documents for AI Search indexing
- **Processed content**: Chunked and embedded content for RAG

## Structure

```
data/
├── README.md                    # This file (included in Git)
├── examples/                    # RAW domain-specific examples (EXCLUDED from Git)
│   ├── *.json                  # Configuration samples
│   └── *.docx                  # Documentation files
├── processed/                   # Processed/chunked content (EXCLUDED from Git)
│   ├── processed_content.json
│   └── processing_summary.json
├── archived/                    # Archived scripts (EXCLUDED from Git)
└── examples-sanitized/          # Generic examples for reference (INCLUDED in Git)
```

## Security Notice

**⚠️ IMPORTANT**: This directory is excluded from Git because it contains:
- Client-specific configuration data
- Database connection strings (even if masked)
- Proprietary technical documentation
- Domain-specific entity names and business logic

## How to Use

### For Development

1. **Create your `data/examples/` directory** with your domain-specific files:
   ```bash
   mkdir -p data/examples
   ```

2. **Add your documentation** (PDFs, DOCX, JSON schemas):
   ```bash
   cp your-domain-docs.docx data/examples/
   cp your-config-schema.json data/examples/
   ```

3. **Process and index** using the provided scripts:
   ```python
   # From project root
   python data/process_document_optimized.py
   python data/reindex_search.py
   ```

### For Adaptation to New Domain

1. **Replace example files** with your domain-specific documents
2. **Update schema descriptions** in `CosmosDbPlugin`
3. **Re-index Azure AI Search** with your documentation
4. **Test queries** against your domain data

## Sanitized Examples

Generic examples are provided in `data/examples-sanitized/` for reference:
- Generic JSON configuration template
- Anonymized environment configuration
- Sample document structure

These examples serve as:
- Reference implementation patterns
- Starting templates for your domain
- Testing scaffolds

## Scripts

### `process_document_optimized.py`
Processes DOCX and JSON files into semantic chunks optimized for RAG (2000-4000 chars).

**Usage:**
```bash
python data/process_document_optimized.py
```

### `reindex_search.py`
Uploads processed chunks to Azure AI Search with embeddings.

**Usage:**
```bash
python data/reindex_search.py
```

## Best Practices

✅ **DO:**
- Keep real data in `data/examples/` (excluded from Git)
- Use generic/anonymized data in `data/examples-sanitized/` (included in Git)
- Document your domain-specific schema in README
- Review `.gitignore` before committing

❌ **DON'T:**
- Commit real client data or credentials
- Include database connection strings
- Push proprietary documentation to public repos
- Remove the `data/` exclusion from `.gitignore`

## Adaptation Checklist

When adapting CORTEX to your domain:

- [ ] Remove existing example files (or keep as reference)
- [ ] Add your domain documentation to `data/examples/`
- [ ] Update JSON schema examples with your entity structure
- [ ] Process documents: `python data/process_document_optimized.py`
- [ ] Index to Azure AI Search: `python data/reindex_search.py`
- [ ] Update `CosmosDbPlugin` with your field names
- [ ] Test queries against your documentation

## Support

For questions about data preparation or indexing:
1. Review [README.md](../README.md) - Customization Guide section
2. Check Azure AI Search documentation
3. Test with sanitized examples first

---

**Version**: 2.0.0 - CORTEX  
**Last Updated**: February 2026
