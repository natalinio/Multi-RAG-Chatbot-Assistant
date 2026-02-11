# Sanitized Examples Directory

This directory contains **generic, anonymized configuration templates** that can be safely included in public repositories.

## ⚠️ Important

These examples are **NOT real configurations** and should be used as:
- Reference templates for understanding structure
- Starting points for creating your domain-specific configurations
- Testing scaffolds for development

## Files

### Configuration Templates

1. **`Generic-Configuration-Bronze-Template.json`**
   - Bronze layer ingestion pattern
   - Incremental load from Azure SQL
   - Partition strategy example

2. **`Generic-Configuration-Silver-Template.json`**
   - Silver layer transformation pattern
   - Aggregation rules and data quality checks
   - Upsert/merge strategy

3. **`Generic-Configuration-Gold-Template.json`**
   - Gold layer analytics pattern
   - SCD Type 2 dimension building
   - Business key and metadata columns

4. **`Generic-Environment-Template.json`**
   - Environment configuration structure
   - Connection string placeholders
   - Security best practices

## How to Use

### As Reference
Review these templates to understand:
- JSON schema structure
- Required vs optional fields
- Configuration patterns (Bronze/Silver/Gold)
- Dependency relationships

### As Starting Point
1. Copy a template to `data/examples/` (excluded from Git)
2. Replace generic values with your domain-specific data
3. Update field names to match your source systems
4. Customize transformation logic

### For Testing
- Use these templates to test the application without real data
- Validate JSON schema compliance
- Test CosmosDbPlugin query patterns
- Experiment with AI Search indexing

## Field Explanations

### Common Fields
- **`domain`**: Data source system identifier (e.g., "DomainA", "DomainB")
- **`entity`**: Unique job/entity name
- **`layer`**: Bronze/Silver/Gold data architecture layer
- **`process_requested`**: Type of operation (ingestion, transformation, load)
- **`market`**: Geographic or business unit identifier
- **`partition`**: Data partitioning strategy
- **`dependencyInbound`**: Upstream jobs that must complete first
- **`dependencyOutbound`**: Downstream jobs that depend on this one

### Bronze Layer (Ingestion)
- **`I1_data_extract_process`**: Source configuration
  - `type`: Connection type (asql, blob, api, etc.)
  - `extraction_type`: Full or Incremental
  - `update_datetime_column`: Column for incremental tracking

### Silver Layer (Transformation)
- **`T1_transformation_process`**: Business logic
- **`T2_data_quality`**: Validation rules
- **`mode-of-write`**: upsert, merge, overwrite

### Gold Layer (Analytics)
- **SCD Type 2**: Slowly Changing Dimension
- **`business_key`**: Natural key for matching
- **`metadata_columns`**: Valid from/to dates, current flag

## Security Best Practices

When creating your real configurations:

✅ **DO:**
- Use Azure Key Vault for secrets
- Use managed identities when possible
- Store configurations in `data/examples/` (excluded from Git)
- Use environment variables for connection strings

❌ **DON'T:**
- Commit real credentials or connection strings
- Include client-specific entity names in public repos
- Hard-code passwords or API keys
- Share proprietary business logic publicly

## Customization

To adapt these templates to your domain:

1. **Update Domain Names**: Replace "DomainA", "DomainB" with your actual systems
2. **Modify Fields**: Add/remove fields based on your schema
3. **Adjust Transformations**: Customize aggregation and validation rules
4. **Set Partitioning**: Define partition strategy for your data volume
5. **Configure Dependencies**: Map your actual job dependencies

## Next Steps

1. Review the [Main README](../../README.md) customization guide
2. Copy templates to `data/examples/` for your use case
3. Update `CosmosDbPlugin` descriptions to match your fields
4. Re-index Azure AI Search with your documentation
5. Test queries against your domain-specific configurations

---

**Note**: These templates are intentionally generic. Real-world configurations will have additional complexity based on your specific business requirements.
