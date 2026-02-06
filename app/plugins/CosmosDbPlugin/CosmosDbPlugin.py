"""
Cosmos DB Plugin for Semantic Kernel.
Provides comprehensive functionality to query Azure Cosmos DB configurations using advanced SQL queries.
Supports filtering, pattern matching, nested fields, arrays, aggregations, and pagination.
"""

import json
import logging
from typing import Any, List, Dict
from semantic_kernel.functions import kernel_function
from ...services.cosmos_service import CosmosService

logger = logging.getLogger(__name__)


class CosmosDbPlugin:
    """
    Semantic Kernel plugin for querying Azure Cosmos DB configurations.
    
    This plugin enables the AI assistant to search and retrieve existing ETL configurations
    stored in Azure Cosmos DB using advanced SQL queries against the 'configurations' container.
    
    Capabilities:
    - Basic filtering (WHERE with =, !=, <, >, <=, >=)
    - Logical operators (AND, OR, NOT)
    - String operations (STARTSWITH, CONTAINS, ENDSWITH, LOWER, UPPER)
    - Array operations (ARRAY_CONTAINS, ARRAY_LENGTH)
    - Nested field navigation (c.I1_data_extract_process.source.type)
    - Pattern matching (IN operator)
    - Sorting (ORDER BY with ASC/DESC)
    - Pagination (OFFSET LIMIT, TOP)
    - Projections (SELECT specific fields, DISTINCT VALUE)
    - Counting via count_configurations() function (application-side)
    
    Limitations:
    - Aggregations (COUNT, SUM, AVG, GROUP BY) NOT supported by Cosmos DB SQL API
    - For counting: use count_configurations() function instead
    """
    
    def __init__(self):
        """
        Initialize the Cosmos DB plugin.
        Creates an instance of CosmosService for database operations.
        """
        self.cosmos_service = CosmosService()
        logger.info("CosmosDbPlugin initialized")
    
    @kernel_function(
        description="""Query Azure Cosmos DB configurations using advanced SQL syntax.
        
        **CRITICAL SYNTAX RULE**: ALWAYS use alias 'c' for the container:
        - ✅ CORRECT: SELECT * FROM c WHERE c.domain = 'SAPBW'
        - ❌ WRONG: SELECT * FROM configurations WHERE domain = 'SAPBW'
        
        **Common Filters:**
        - c.domain: Domain identifier (NielsenUS, NielsenGB, SAPBW, Profisee, SFAsseco, SFAmalia)
        - c.layer: Data layer (Bronze, Silver, Gold)
        - c.entity: Entity/job name (unique identifier for document)
        - c.process_requested: Process type (ingestion, transformation, validation, integration, load)
        - c.market: Market code (US, GB, GLB, MDATTR, MDTXT, etc.)
        - c.partition: Array of partition values for data segmentation
        - c.dependencyInbound: Array of upstream job dependencies
        - c.dependencyOutbound: Array of downstream job dependencies
        - c._ts: Timestamp for sorting recent configs
        
        **Supported Operations:**
        
        1. BASIC FILTERING:
           SELECT * FROM c WHERE c.domain = 'SAPBW' AND c.layer = 'Bronze'
           SELECT * FROM c WHERE c.market = 'US' OR c.market = 'GB'
        
        2. STRING OPERATIONS (case-insensitive matching):
           SELECT * FROM c WHERE STARTSWITH(c.entity, 'Validation')
           SELECT * FROM c WHERE CONTAINS(LOWER(c.entity), 'aggregated')
           SELECT * FROM c WHERE ENDSWITH(c.entity, 'Vodka')
        
        3. NESTED FIELDS (access configuration details):
           SELECT * FROM c WHERE c.I1_data_extract_process.source.type = 'asql'
           SELECT * FROM c WHERE c.D3_load_data_process['mode-of-write'] = 'upsert'
           SELECT * FROM c WHERE c.D3_load_data_process['target-path'] = 'catalog.schema.table'
        
        4. ARRAY OPERATIONS (dependencies and partitions):
           SELECT * FROM c WHERE ARRAY_CONTAINS(c.partition, 'Spirits')
           SELECT * FROM c WHERE ARRAY_CONTAINS(c.dependencyInbound, 'ValidationMarketDim-NielsenAT-Bronze-Spirits')
           SELECT * FROM c WHERE ARRAY_LENGTH(c.dependencyInbound) > 0
        
        5. IN OPERATOR (multiple values):
           SELECT * FROM c WHERE c.domain IN ('NielsenUS', 'NielsenGB', 'SAPBW')
           SELECT * FROM c WHERE c.layer NOT IN ('Gold')
        
        6. SORTING (most recent first):
           SELECT * FROM c WHERE c.domain = 'SAPBW' ORDER BY c._ts DESC
           SELECT * FROM c ORDER BY c.entity ASC
        
        7. PROJECTION (specific fields only):
           SELECT c.id, c.domain, c.entity, c.layer FROM c
           SELECT VALUE c.entity FROM c WHERE c.domain = 'NielsenUS'
        
        8. PAGINATION (limit results):
           SELECT TOP 10 * FROM c WHERE c.domain = 'SAPBW' ORDER BY c._ts DESC
           SELECT * FROM c ORDER BY c._ts DESC OFFSET 10 LIMIT 20
        
        **Real-World Use Cases:**
        
        Use Case 1: "Find all Bronze layer configurations for SAPBW domain"
        Query: SELECT * FROM c WHERE c.domain = 'SAPBW' AND c.layer = 'Bronze' ORDER BY c._ts DESC
        
        Use Case 2: "Show me configurations with Azure SQL as data source"
        Query: SELECT * FROM c WHERE c.I1_data_extract_process.source.type = 'asql'
        
        Use Case 3: "Find validation jobs for Nielsen markets"
        Query: SELECT * FROM c WHERE STARTSWITH(c.entity, 'Validation') AND CONTAINS(c.entity, 'Nielsen')
        
        Use Case 4: "Get Silver layer configs with upsert mode"
        Query: SELECT * FROM c WHERE c.layer = 'Silver' AND c.D3_load_data_process['mode-of-write'] = 'upsert'
        
        Use Case 5: "Find all jobs that depend on a specific upstream job"
        Query: SELECT * FROM c WHERE ARRAY_CONTAINS(c.dependencyInbound, 'ValidationMarketDim-NielsenAT-Bronze-Spirits')
        
        Use Case 6: "Find jobs writing to a specific Unity Catalog table"
        Query: SELECT * FROM c WHERE CONTAINS(c.D3_load_data_process['target-path'], 'catalog.schema.table')
        
        Use Case 7: "Find entities with 'Aggregated' in the name (case-insensitive)"
        Query: SELECT * FROM c WHERE CONTAINS(LOWER(c.entity), 'aggregated')
        
        Use Case 8: "Get 10 most recent configurations across all domains"
        Query: SELECT TOP 10 * FROM c ORDER BY c._ts DESC
        
        **Best Practices:**
        - Always include WHERE clause for performance
        - Use ORDER BY c._ts DESC for most recent configs
        - Use OFFSET/LIMIT or TOP for pagination
        - Use LOWER() for case-insensitive string matching
        - Project only needed fields to reduce payload
        - Use ARRAY_CONTAINS for dependency queries
        
        **Limitations:**
        - Aggregations (COUNT, GROUP BY, SUM, AVG) are NOT supported
        - For counting, retrieve results and count in application code
        - Complex JOINs are not supported in Cosmos DB SQL API
        """,
        name="query_configurations"
    )
    async def query_existing_config(self, sql_query: str) -> str:
        """
        Execute an advanced SQL query against the Cosmos DB configurations container.
        
        Args:
            sql_query (str): SQL query string with Cosmos DB SQL syntax.
                           MUST use 'c' alias: SELECT * FROM c WHERE c.field = 'value'
                           Supports nested fields, arrays, aggregations, and advanced filtering.
        
        Returns:
            str: JSON string containing the query results with metadata:
                 - success: boolean indicating query success
                 - query: the executed SQL query
                 - count: number of results returned
                 - results: array of configuration documents
                 - error: error message if query failed
                 - hint: helpful suggestion if no results found
        
        Examples:
            >>> query = "SELECT * FROM c WHERE c.domain = 'SAPBW' AND c.layer = 'Bronze'"
            >>> result = await query_existing_config(query)
        """
        try:
            logger.info(f"Executing Cosmos DB SQL query: {sql_query}")
            
            # Validate query is not empty
            if not sql_query or not sql_query.strip():
                error_msg = "SQL query cannot be empty"
                logger.error(error_msg)
                return json.dumps({
                    "success": False,
                    "error": error_msg,
                    "results": []
                }, indent=2)
            
            # ✅ HIGH PRIORITY VALIDATION A: Block unsupported aggregation functions
            sql_upper = sql_query.upper()
            unsupported_aggregations = []
            if 'COUNT(' in sql_upper:
                unsupported_aggregations.append('COUNT()')
            if 'SUM(' in sql_upper:
                unsupported_aggregations.append('SUM()')
            if 'AVG(' in sql_upper:
                unsupported_aggregations.append('AVG()')
            if 'MIN(' in sql_upper:
                unsupported_aggregations.append('MIN()')
            if 'MAX(' in sql_upper:
                unsupported_aggregations.append('MAX()')
            if 'GROUP BY' in sql_upper:
                unsupported_aggregations.append('GROUP BY')
            
            if unsupported_aggregations:
                error_msg = f"Aggregation functions are not supported by Cosmos DB SQL API: {', '.join(unsupported_aggregations)}"
                logger.error(f"Blocked unsupported aggregation query: {sql_query}")
                return json.dumps({
                    "success": False,
                    "error": error_msg,
                    "blocked_query": sql_query,
                    "unsupported_features": unsupported_aggregations,
                    "solution": "Use count_configurations() function for counting instead",
                    "example": "await count_configurations(filter=\"c.domain = 'NielsenGB'\")",
                    "results": []
                }, indent=2)
            
            # Validate query uses 'c' alias (common mistake detection)
            sql_lower = sql_query.lower()
            if 'from c' not in sql_lower and 'from configurations' in sql_lower:
                error_msg = "Invalid query syntax. Must use alias 'c': SELECT * FROM c WHERE..."
                logger.error(error_msg)
                return json.dumps({
                    "success": False,
                    "error": error_msg,
                    "hint": "Change 'FROM configurations' to 'FROM c'",
                    "corrected_query": sql_query.replace('configurations', 'c').replace('CONFIGURATIONS', 'c'),
                    "results": []
                }, indent=2)
            
            # Execute the query
            results = await self.cosmos_service.query_configurations(sql_query)
            
            # 🛡️ TOKEN SAFETY: Limit results to prevent token overflow
            MAX_RESULTS = 50  # Maximum configurations to return in one response
            total_results = len(results)
            truncated = False
            
            if total_results > MAX_RESULTS:
                logger.warning(f"Truncating results from {total_results} to {MAX_RESULTS} to prevent token overflow")
                results = results[:MAX_RESULTS]
                truncated = True
            
            # Format response
            response = {
                "success": True,
                "query": sql_query,
                "total_found": total_results,
                "count": len(results),
                "results": results
            }
            
            logger.info(f"Query executed successfully. Found {total_results} configurations, returning {len(results)}.")
            
            # Add truncation warning if applicable
            if truncated:
                response["warning"] = f"⚠️ Results truncated from {total_results} to {MAX_RESULTS} configurations to prevent token overflow."
                response["suggestion"] = "Refine your query with more specific filters (domain, layer, market) or use TOP/LIMIT clause to control result size."
            
            # Add helpful hints if no results
            if len(results) == 0:
                response["hint"] = "No results found. Try: 1) Broadening filter criteria, 2) Checking field names (case-sensitive), 3) Using LOWER() for case-insensitive matching"
            
            return json.dumps(response, indent=2, default=str)
            
        except Exception as e:
            error_msg = f"Error executing Cosmos DB query: {str(e)}"
            logger.error(error_msg, exc_info=True)
            
            error_response = {
                "success": False,
                "error": error_msg,
                "query": sql_query,
                "results": [],
                "troubleshooting": [
                    "Verify field names match document structure (case-sensitive)",
                    "Ensure 'c' alias is used: FROM c",
                    "Check for typos in field names or values",
                    "Verify nested field paths are correct (e.g., c.I1_data_extract_process.source1.type)",
                    "For arrays, use ARRAY_CONTAINS(c.partition, 'value')"
                ]
            }
            
            return json.dumps(error_response, indent=2)
    
    @kernel_function(
        description="List configurations by domain with optional limit.",
        name="list_by_domain"
    )
    async def list_configurations_by_domain(self, domain: str, limit: str = "20") -> str:
        """
        List configurations filtered by domain.
        
        Args:
            domain (str): The domain to filter by (e.g., 'NielsenUS', 'Profisee')
            limit (str): Maximum number of results to return (default: "20")
        
        Returns:
            str: JSON string containing the filtered configurations
        """
        try:
            # ✅ HIGH PRIORITY VALIDATION H: Validate domain exists with suggestions
            KNOWN_DOMAINS = [
                'NielsenUS', 'NielsenGB', 'NielsenBR', 'NielsenAT', 'NielsenBE', 'NielsenDE', 
                'NielsenES', 'NielsenFR', 'NielsenIT', 'NielsenMX', 'NielsenNL', 'NielsenPL', 
                'NielsenPT', 'SAPBW', 'Profisee', 'SFAsseco', 'SFAmalia', 
                'ITOperations', 'IWSR', 'MasterData', 'NABCA', 'PBI', 'RGMPtC_DRE', 
                'RGMPtC_FPC', 'RetailerAsda', 'RetailerAuchan', 'RetailerCarrefour', 
                'RetailerDIA', 'RetailerECI', 'RetailerMorrisons', 'RetailerSainsbury', 
                'RetailerTesco', 'TM1', 'com_smile'
            ]
            
            domain_warning = None  # Store warning to include in final response
            
            if domain not in KNOWN_DOMAINS:
                # Fuzzy match for suggestions
                import difflib
                suggestions = difflib.get_close_matches(domain, KNOWN_DOMAINS, n=3, cutoff=0.6)
                
                logger.warning(f"Domain '{domain}' not found in known domains. Suggestions: {suggestions}")
                
                # Create warning to include in response
                domain_warning = {
                    "warning": f"Domain '{domain}' not found in known domains",
                    "did_you_mean": suggestions if suggestions else None,
                    "known_domains": KNOWN_DOMAINS[:10],  # Show first 10 for brevity
                    "note": "Query executed but may return empty results if domain is incorrect",
                    "suggestion": "Check domain spelling (case-sensitive) or use one of the known domains"
                }
                
                # If no close matches, return warning immediately without querying
                if not suggestions or len(suggestions) == 0:
                    return json.dumps({
                        **domain_warning,
                        "success": False,
                        "domain": domain,
                        "count": 0,
                        "results": []
                    }, indent=2)
            
            # Convert limit to integer with validation
            try:
                limit_int = int(limit)
                if limit_int <= 0:
                    limit_int = 20
                elif limit_int > 1000:  # Prevent excessive queries
                    limit_int = 1000
            except (ValueError, TypeError):
                limit_int = 20
            
            logger.info(f"Listing configurations for domain: {domain}, limit: {limit_int}")
            
            # Use the CosmosService method for domain filtering
            results = await self.cosmos_service.list_configurations_by_domain(domain, limit_int)
            
            response = {
                "success": True,
                "domain": domain,
                "limit": limit_int,
                "count": len(results),
                "results": results
            }
            
            # Include domain warning if present
            if domain_warning:
                response = {**domain_warning, **response}
            
            logger.info(f"Retrieved {len(results)} configurations for domain: {domain}")
            
            return json.dumps(response, indent=2, default=str)
            
        except Exception as e:
            error_msg = f"Error listing configurations by domain: {str(e)}"
            logger.error(error_msg)
            
            error_response = {
                "success": False,
                "error": error_msg,
                "domain": domain,
                "results": []
            }
            
            return json.dumps(error_response, indent=2)
    
    @kernel_function(
        description="""Count configurations matching specific criteria.
        
        Since Cosmos DB SQL API does not support COUNT aggregations, this function:
        1. Executes a SELECT query to retrieve matching documents
        2. Counts the results in application code
        3. Returns the count along with summary statistics
        
        **Use this function when users ask "how many" or "count" questions.**
        
        Examples:
        - "How many configs for NielsenGB?" 
          → filter: "c.domain = 'NielsenGB'"
        
        - "How many Bronze layer configs?"
          → filter: "c.layer = 'Bronze'"
        
        - "How many ASQL ingestion configs?"
          → filter: "c.I1_data_extract_process.source.type = 'ASQL'"
        
        - "Count all configs"
          → filter: "" (empty = no filter)
        
        **IMPORTANT**: Provide the WHERE clause condition WITHOUT the "WHERE" keyword.
        Example: "c.domain = 'NielsenGB' AND c.layer = 'Bronze'"
        
        Args:
            filter (str): WHERE clause condition (without WHERE keyword). Leave empty for all.
        
        Returns:
            JSON with count, distinct values for common fields, and sample entities.
        """,
        name="count_configurations"
    )
    async def count_configurations(self, filter: str = "") -> str:
        """
        Count configurations matching a filter criteria.
        
        Args:
            filter (str): WHERE clause condition without WHERE keyword
        
        Returns:
            str: JSON with count and statistics
        """
        try:
            # ✅ HIGH PRIORITY VALIDATION E: Block aggregation functions in filter
            if filter and filter.strip():
                filter_upper = filter.upper()
                unsupported_in_filter = []
                if 'COUNT(' in filter_upper:
                    unsupported_in_filter.append('COUNT()')
                if 'SUM(' in filter_upper:
                    unsupported_in_filter.append('SUM()')
                if 'AVG(' in filter_upper:
                    unsupported_in_filter.append('AVG()')
                if 'MIN(' in filter_upper:
                    unsupported_in_filter.append('MIN()')
                if 'MAX(' in filter_upper:
                    unsupported_in_filter.append('MAX()')
                if 'GROUP BY' in filter_upper:
                    unsupported_in_filter.append('GROUP BY')
                
                if unsupported_in_filter:
                    error_msg = f"Cannot use aggregation functions in filter parameter: {', '.join(unsupported_in_filter)}"
                    logger.error(f"Blocked aggregation in count filter: {filter}")
                    return json.dumps({
                        "success": False,
                        "error": error_msg,
                        "invalid_filter": filter,
                        "unsupported_features": unsupported_in_filter,
                        "suggestion": "Provide simple WHERE conditions without aggregations",
                        "example": "c.domain = 'NielsenGB' AND c.layer = 'Bronze'",
                        "note": "The count_configurations() function counts results automatically. Just provide filter conditions.",
                        "total_count": 0
                    }, indent=2)
            
            # Build the query
            if filter and filter.strip():
                # Validate filter starts with 'c.'
                if not filter.strip().startswith('c.'):
                    filter = f"c.{filter}"
                
                query = f"SELECT * FROM c WHERE {filter}"
            else:
                query = "SELECT * FROM c"
            
            logger.info(f"Counting configurations with filter: {filter if filter else 'none'}")
            
            # Execute query
            results = await self.cosmos_service.query_configurations(query)
            
            # Count and analyze results
            total_count = len(results)
            
            # Extract statistics
            domains = set()
            layers = set()
            markets = set()
            process_types = set()
            entities = []
            
            for doc in results:
                if 'domain' in doc:
                    domains.add(doc['domain'])
                if 'layer' in doc:
                    layers.add(doc['layer'])
                if 'market' in doc:
                    markets.add(doc['market'])
                if 'process_requested' in doc:
                    process_types.add(doc['process_requested'])
                if 'entity' in doc and len(entities) < 5:
                    entities.append(doc['entity'])
            
            response = {
                "success": True,
                "query_used": query,
                "filter_applied": filter if filter else "none (all configurations)",
                "total_count": total_count,
                "statistics": {
                    "unique_domains": sorted(list(domains)),
                    "unique_layers": sorted(list(layers)),
                    "unique_markets": sorted(list(markets)),
                    "unique_process_types": sorted(list(process_types))
                },
                "sample_entities": entities,
                "note": "Cosmos DB does not support COUNT aggregation natively. This count was computed in application code."
            }
            
            logger.info(f"Count complete: {total_count} configurations matched")
            
            return json.dumps(response, indent=2, default=str)
            
        except Exception as e:
            error_msg = f"Error counting configurations: {str(e)}"
            logger.error(error_msg, exc_info=True)
            
            error_response = {
                "success": False,
                "error": error_msg,
                "filter": filter,
                "total_count": 0
            }
            
            return json.dumps(error_response, indent=2)
    
    @kernel_function(
        description="""Get comprehensive schema information and query examples for the configurations container.
        
        Returns detailed documentation about:
        - Container structure and all common fields with descriptions
        - Nested configuration structures for Bronze, Silver, and Gold layers
        - Supported query patterns with examples
        - Real-world use cases and queries
        - Best practices and common mistakes to avoid
        - Field value examples for common attributes
        """,
        name="get_schema_info"
    )
    async def get_schema_info(self) -> str:
        """
        Provide comprehensive schema information and query examples.
        
        Returns:
            str: JSON string with complete schema documentation, examples, and best practices
        """
        schema_info = {
            "container_name": "configurations",
            "description": "ETL configuration metadata for Bronze, Silver, and Gold layers",
            
            "common_fields": {
                "id": "Unique document identifier (string)",
                "domain": "Data domain identifier (e.g., NielsenUS, NielsenGB, SAPBW, Profisee, SFAsseco, SFAmalia)",
                "entity": "Entity job name - uniquely identifies a single json document (string)",
                "layer": "Data layer of the medallion architecture (Bronze, Silver, Gold)",
                "process_requested": "Type of processing requested (ingestion, transformation, validation, integration, load)",
                "market": "Market identifier - used to partition domain data (US, GB, GLB, MDATTR, MDTXT, etc.)",
                "partition": "Sub-partition attribute for further data segmentation (array of strings)",
                "dependencyInbound": "Inbound dependencies - list of entity job names this job depends on (array)",
                "dependencyOutbound": "Outbound dependencies - list of jobs that depend on this one (array)",
                "_ts": "Timestamp of last modification (unix epoch)"
            },
            
            "nested_structures": {
                "Bronze_layer": {
                    "I0_common_conf": "Common configuration (use-case, prcs-name, table_name)",
                    "I1_data_extract_process": "Source extraction config with sourceList array and source details",
                    "I2_load_data_process": "Data load configuration (mode-of-write, target-path, target-format, loadType)"
                },
                "Silver_layer": {
                    "D0_common_conf": "Common configuration",
                    "D1_data_extract_process": "Data extraction from Bronze layer",
                    "D2_data_transform_process": "Transformation rules (transform-list, T1, T2, etc.)",
                    "D3_load_data_process": "Load to Silver (mode-of-write: upsert, merge, append)"
                }
            },
            
            "query_patterns": {
                "basic_filtering": [
                    "SELECT * FROM c WHERE c.domain = 'SAPBW'",
                    "SELECT * FROM c WHERE c.layer = 'Bronze' AND c.market = 'US'",
                    "SELECT * FROM c WHERE c.process_requested = 'ingestion'"
                ],
                "string_operations": [
                    "SELECT * FROM c WHERE STARTSWITH(c.entity, 'Validation')",
                    "SELECT * FROM c WHERE CONTAINS(LOWER(c.entity), 'aggregated')",
                    "SELECT * FROM c WHERE ENDSWITH(c.entity, 'Vodka')"
                ],
                "nested_fields": [
                    "SELECT * FROM c WHERE c.I1_data_extract_process.source.type = 'asql'",
                    "SELECT * FROM c WHERE c.D3_load_data_process['mode-of-write'] = 'upsert'",
                    "SELECT * FROM c WHERE c.I2_load_data_process['target-format'] = 'delta'",
                    "SELECT * FROM c WHERE CONTAINS(c.D3_load_data_process['target-path'], 'catalog.schema.table')"
                ],
                "array_operations": [
                    "SELECT * FROM c WHERE ARRAY_CONTAINS(c.partition, 'Spirits')",
                    "SELECT * FROM c WHERE ARRAY_CONTAINS(c.dependencyInbound, 'ValidationMarketDim-NielsenAT-Bronze-Spirits')",
                    "SELECT * FROM c WHERE ARRAY_LENGTH(c.dependencyInbound) > 0",
                    "SELECT * FROM c WHERE ARRAY_LENGTH(c.partition) = 0"
                ],
                "in_operator": [
                    "SELECT * FROM c WHERE c.domain IN ('NielsenUS', 'NielsenGB', 'SAPBW')",
                    "SELECT * FROM c WHERE c.market IN ('US', 'GB', 'GLB')",
                    "SELECT * FROM c WHERE c.layer NOT IN ('Gold')"
                ],
                "sorting_pagination": [
                    "SELECT TOP 10 * FROM c ORDER BY c._ts DESC",
                    "SELECT * FROM c WHERE c.domain = 'SAPBW' ORDER BY c.entity ASC",
                    "SELECT * FROM c ORDER BY c._ts DESC OFFSET 10 LIMIT 20"
                ],
                "projections": [
                    "SELECT c.id, c.domain, c.entity, c.layer FROM c",
                    "SELECT VALUE c.entity FROM c WHERE c.domain = 'NielsenUS'",
                    "SELECT c.entity, c.market, c.partition FROM c WHERE c.layer = 'Bronze'"
                ]
            },
            
            "real_world_use_cases": [
                {
                    "question": "Find all Bronze layer configurations for SAPBW domain",
                    "query": "SELECT * FROM c WHERE c.domain = 'SAPBW' AND c.layer = 'Bronze' ORDER BY c._ts DESC"
                },
                {
                    "question": "Show me configurations with Azure SQL as data source",
                    "query": "SELECT * FROM c WHERE c.I1_data_extract_process.source.type = 'asql'"
                },
                {
                    "question": "Find all validation jobs for Nielsen markets",
                    "query": "SELECT * FROM c WHERE STARTSWITH(c.entity, 'Validation') AND CONTAINS(c.entity, 'Nielsen')"
                },
                {
                    "question": "Get Silver layer configs with upsert mode",
                    "query": "SELECT * FROM c WHERE c.layer = 'Silver' AND c.D3_load_data_process['mode-of-write'] = 'upsert'"
                },
                {
                    "question": "Find all jobs that depend on a specific upstream job",
                    "query": "SELECT * FROM c WHERE ARRAY_CONTAINS(c.dependencyInbound, 'ValidationMarketDim-NielsenAT-Bronze-Spirits')"
                },
                {
                    "question": "Find jobs writing to a specific Unity Catalog table",
                    "query": "SELECT * FROM c WHERE CONTAINS(c.D3_load_data_process['target-path'], 'catalog.schema.table')"
                },
                {
                    "question": "Find entities with 'Aggregated' in the name (case-insensitive)",
                    "query": "SELECT * FROM c WHERE CONTAINS(LOWER(c.entity), 'aggregated')"
                },
                {
                    "question": "Get 10 most recent configurations across all domains",
                    "query": "SELECT TOP 10 * FROM c ORDER BY c._ts DESC"
                },
                {
                    "question": "Find Bronze ingestion jobs for Nielsen US market",
                    "query": "SELECT * FROM c WHERE c.domain = 'NielsenUS' AND c.layer = 'Bronze' AND c.process_requested = 'ingestion'"
                },
                {
                    "question": "Find configs with Spirits partition",
                    "query": "SELECT * FROM c WHERE ARRAY_CONTAINS(c.partition, 'Spirits')"
                },
                {
                    "question": "Find all Salesforce ingestion configurations",
                    "query": "SELECT * FROM c WHERE c.I1_data_extract_process.source.type = 'salesforce'"
                },
                {
                    "question": "Get configs with delta format in target",
                    "query": "SELECT * FROM c WHERE c.I2_load_data_process['target-format'] = 'delta'"
                }
            ],
            
            "best_practices": [
                "Always include WHERE clause for performance optimization",
                "Use ORDER BY c._ts DESC to get most recent configurations",
                "Use OFFSET/LIMIT or TOP for pagination with large result sets",
                "Project only needed fields (SELECT c.id, c.domain...) to reduce payload",
                "Use LOWER() with CONTAINS for case-insensitive matching",
                "Leverage ARRAY_CONTAINS for partition and dependency filtering",
                "Combine multiple conditions with AND/OR for complex queries",
                "Use IN operator for multiple value matching",
                "Always use alias 'c' (FROM c) as per Cosmos DB syntax",
                "For nested fields use bracket notation for fields with hyphens: c.field['sub-field']"
            ],
            
            "limitations": [
                "Aggregations (COUNT, GROUP BY, SUM, AVG, MIN, MAX) are NOT supported",
                "To count results, retrieve documents and count in application code",
                "Complex JOINs are not available in Cosmos DB SQL API",
                "Subqueries are not supported"
            ],
            
            "common_mistakes": [
                {
                    "wrong": "SELECT * FROM configurations WHERE domain = 'SAPBW'",
                    "correct": "SELECT * FROM c WHERE c.domain = 'SAPBW'",
                    "reason": "Must use alias 'c' for container"
                },
                {
                    "wrong": "SELECT * FROM c WHERE I1_data_extract_process.type = 'asql'",
                    "correct": "SELECT * FROM c WHERE c.I1_data_extract_process.source1.type = 'asql'",
                    "reason": "Must prefix all fields with 'c.' and use correct nested path"
                },
                {
                    "wrong": "SELECT * FROM c WHERE partition = 'US'",
                    "correct": "SELECT * FROM c WHERE ARRAY_CONTAINS(c.partition, 'US')",
                    "reason": "partition is an array, must use ARRAY_CONTAINS"
                },
                {
                    "wrong": "SELECT * FROM c WHERE c.entity LIKE '%Aggregated%'",
                    "correct": "SELECT * FROM c WHERE CONTAINS(LOWER(c.entity), 'aggregated')",
                    "reason": "LIKE is not fully supported, use CONTAINS with LOWER for case-insensitive"
                },
                {
                    "wrong": "SELECT COUNT(1) as total FROM c",
                    "correct": "SELECT * FROM c (then count in code)",
                    "reason": "COUNT and aggregations are not supported in Cosmos DB SQL API"
                }
            ],
            
            "field_value_examples": {
                "domains": ["NielsenUS", "NielsenGB", "NielsenBR", "NielsenAT", "SAPBW", "Profisee", "SFAsseco", "SFAmalia"],
                "layers": ["Bronze", "Silver", "Gold"],
                "process_requested": ["ingestion", "transformation", "validation", "integration", "load"],
                "markets": ["US", "GB", "GLB", "MDATTR", "MDTXT", "BR", "AT"],
                "partitions": ["Spirits", "Vodka", "SparklingWine", "RTD", "GLB"],
                "source_types": ["asql", "salesforce", "adls", "profisee", "jdbc"]
            }
        }
        
        return json.dumps(schema_info, indent=2)
    
    @kernel_function(
        description="""Generate a dependency graph (network diagram) for jobs in a specific domain.
        
        This function creates a Mermaid diagram showing the dependency relationships between jobs.
        Jobs are colored by layer (Bronze/Silver/Gold) and connected based on dependencyInbound.
        
        IMPORTANT: 
        - This function retrieves ONLY essential fields (entity, dependencyInbound, layer, domain, process_request) to avoid token saturation
        - DO NOT use get_configurations_by_domain for dependency graph queries
        - The function returns a formatted response with an EMBEDDED Mermaid diagram that will be automatically rendered by the UI
        - You MUST include the entire response (including the ```mermaid block) directly in your answer without modifications
        - DO NOT explain the diagram or add extra context - just pass through the response as-is
        
        Use Cases:
        - "Show me the dependency graph for SAPBW domain"
        - "Draw the dependency network for NielsenGB Bronze layer"
        - "Visualize job dependencies in Profisee domain across all layers"
        - "Show Bronze and Silver job dependencies in SFAsseco"
        - "Graph the connections between Gold layer jobs in SAPBW"
        
        Args:
            domain (str): The domain to filter by (e.g., "SAPBW", "NielsenGB", "Profisee")
            layers (str, optional): Comma-separated layer filter (e.g., "Bronze", "Bronze,Silver", "Gold")
        
        Returns:
            str: Formatted text with embedded Mermaid diagram and statistics
        
        Examples:
            >>> graph = await generate_dependency_graph(domain="SAPBW")
            >>> graph = await generate_dependency_graph(domain="NielsenGB", layers="Bronze")
            >>> graph = await generate_dependency_graph(domain="Profisee", layers="Bronze,Silver")
        """
    )
    async def generate_dependency_graph(self, domain: str, layers: str = None) -> str:
        """
        Generate a Mermaid dependency graph for jobs in a domain.
        
        Args:
            domain (str): Domain to filter configurations
            layers (str, optional): Comma-separated layer filter (e.g., "Bronze,Silver")
            
        Returns:
            str: JSON with Mermaid diagram and metadata
        """
        try:
            logger.info(f"Generating dependency graph for domain: {domain}, layers: {layers or 'all'}")
            
            # Parse layers parameter
            layer_list = []
            if layers:
                layer_list = [l.strip() for l in layers.split(',')]
            
            # Build query - retrieve ONLY essential fields to avoid token saturation
            # Fields: entity, dependencyInbound, layer, domain, process_request
            if layer_list:
                layer_condition = " OR ".join([f"c.layer = '{l}'" for l in layer_list])
                query = f"SELECT c.entity, c.dependencyInbound, c.layer, c.domain, c.process_request FROM c WHERE c.domain = '{domain}' AND ({layer_condition})"
            else:
                query = f"SELECT c.entity, c.dependencyInbound, c.layer, c.domain, c.process_request FROM c WHERE c.domain = '{domain}'"
            
            # Execute query
            results = await self.cosmos_service.query_configurations(query)
            
            if not results:
                layer_info = f" and layers '{layers}'" if layers else ""
                return json.dumps({
                    "success": False,
                    "error": f"No configurations found for domain '{domain}'{layer_info}",
                    "suggestion": "Try without layer filter or check domain/layer names"
                }, indent=2)
            
            # Build graph using only dependencyInbound
            # Track nodes with their layer info
            nodes_with_layer = {}  # entity -> layer
            edges = []
            
            for config in results:
                entity = config.get('entity', 'Unknown')
                layer = config.get('layer', 'Unknown')
                nodes_with_layer[entity] = layer
                
                # Add inbound dependencies (jobs that must run BEFORE this entity)
                inbound = config.get('dependencyInbound', [])
                if inbound:
                    for dep in inbound:
                        # We might not have layer info for dependency if it's outside our filter
                        if dep not in nodes_with_layer:
                            nodes_with_layer[dep] = 'Unknown'
                        edges.append((dep, entity))
            
            # Remove duplicate edges
            edges = list(set(edges))
            
            # Calculate stats by layer
            layer_stats = {}
            for node, layer in nodes_with_layer.items():
                layer_stats[layer] = layer_stats.get(layer, 0) + 1
            
            # Check if graph is too large for display
            MAX_NODES_FOR_DIAGRAM = 50
            if len(nodes_with_layer) > MAX_NODES_FOR_DIAGRAM:
                # Too many nodes - provide summary instead
                layer_breakdown = ", ".join([f"{count} {layer}" for layer, count in sorted(layer_stats.items())])
                return f"""⚠️ The dependency graph for **{domain}** domain{f" ({layers} layers)" if layers else " (all layers)"} is too large to visualize ({len(nodes_with_layer)} jobs, {len(edges)} dependencies).

**Suggestion**: Please filter by specific process_request or use a more specific layer combination.

**Stats**: {len(nodes_with_layer)} jobs, {len(edges)} dependencies ({layer_breakdown})

**Example queries**:
- "Show dependency graph for SAPBW Bronze layer only"
- "Show dependency graph for jobs in SAPBW GTN process"
- "Visualize dependencies for SAPBW Silver MDATTR jobs"
"""
            
            # Define layer colors (Bronze, Silver, Gold)
            layer_colors = {
                'Bronze': '#CD7F32',
                'Silver': '#C0C0C0',
                'Gold': '#FFD700',
                'Unknown': '#808080'
            }
            
            # Generate Mermaid diagram with styled nodes
            mermaid_lines = ["```mermaid", "graph LR"]
            
            # Add style definitions for each layer
            mermaid_lines.append("    classDef bronzeStyle fill:#CD7F32,stroke:#8B5A2B,stroke-width:2px,color:#000")
            mermaid_lines.append("    classDef silverStyle fill:#C0C0C0,stroke:#808080,stroke-width:2px,color:#000")
            mermaid_lines.append("    classDef goldStyle fill:#FFD700,stroke:#DAA520,stroke-width:2px,color:#000")
            mermaid_lines.append("    classDef unknownStyle fill:#808080,stroke:#404040,stroke-width:2px,color:#fff")
            mermaid_lines.append("")
            
            # Track which nodes have been added
            added_nodes = set()
            
            # Add edges (connections) with styled nodes
            for source, target in sorted(edges):
                source_id = source.replace('-', '_').replace('.', '_').replace(' ', '_')
                target_id = target.replace('-', '_').replace('.', '_').replace(' ', '_')
                
                source_layer = nodes_with_layer.get(source, 'Unknown')
                target_layer = nodes_with_layer.get(target, 'Unknown')
                
                mermaid_lines.append(f"    {source_id}[\"{source}\"] --> {target_id}[\"{target}\"]")
                
                # Add style classes
                if source_id not in added_nodes:
                    style_class = f"{source_layer.lower()}Style" if source_layer in layer_colors else "unknownStyle"
                    mermaid_lines.append(f"    class {source_id} {style_class}")
                    added_nodes.add(source_id)
                
                if target_id not in added_nodes:
                    style_class = f"{target_layer.lower()}Style" if target_layer in layer_colors else "unknownStyle"
                    mermaid_lines.append(f"    class {target_id} {style_class}")
                    added_nodes.add(target_id)
            
            # Add isolated nodes (nodes with no dependencies)
            all_connected_nodes = set([e[0] for e in edges]) | set([e[1] for e in edges])
            isolated_nodes = set(nodes_with_layer.keys()) - all_connected_nodes
            
            if isolated_nodes:
                mermaid_lines.append("")
                for node in sorted(isolated_nodes):
                    node_id = node.replace('-', '_').replace('.', '_').replace(' ', '_')
                    node_layer = nodes_with_layer[node]
                    mermaid_lines.append(f"    {node_id}[\"{node}\"]")
                    style_class = f"{node_layer.lower()}Style" if node_layer in layer_colors else "unknownStyle"
                    mermaid_lines.append(f"    class {node_id} {style_class}")
            
            mermaid_lines.append("```")
            mermaid_diagram = "\n".join(mermaid_lines)
            
            # Build concise response with embedded diagram (layer_stats already calculated above)
            layer_breakdown = ", ".join([f"{count} {layer}" for layer, count in sorted(layer_stats.items())])
            
            response_text = f"""Here is the dependency graph for **{domain}** domain{f" ({layers} layers)" if layers else " (all layers)"}:

{mermaid_diagram}

**Stats**: {len(nodes_with_layer)} jobs, {len(edges)} dependencies ({layer_breakdown})  
**Legend**: 🟫 Bronze | ⚪ Silver | 🟨 Gold | ⬜ External dependencies"""
            
            logger.info(f"Dependency graph generated: {len(nodes_with_layer)} nodes, {len(edges)} edges, layers: {layer_stats}")
            
            return response_text
            
        except Exception as e:
            error_msg = f"Error generating dependency graph: {str(e)}"
            logger.error(error_msg, exc_info=True)
            return f"❌ Error generating dependency graph for domain '{domain}': {error_msg}"
    
    async def cleanup(self):
        """
        Clean up resources used by the plugin.
        Should be called when the plugin is no longer needed.
        """
        try:
            await self.cosmos_service.close()
            logger.info("CosmosDbPlugin cleanup completed")
        except Exception as e:
            logger.error(f"Error during CosmosDbPlugin cleanup: {str(e)}")