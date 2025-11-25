"""
ETL Configuration Plugin for Semantic Kernel.
Implements RAG (Retrieval Augmented Generation) using Azure AI Search for ETL documentation.
"""

import json
import logging
from typing import List, Dict, Any, Optional
from semantic_kernel.functions import kernel_function
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
from ...core.config import get_settings

logger = logging.getLogger(__name__)


class EtlConfigPlugin:
    """
    Semantic Kernel plugin for ETL configuration assistance using RAG.
    
    This plugin searches through indexed ETL documentation to provide
    guidance on configuration parameters, schemas, and best practices.
    """
    
    def __init__(self):
        """
        Initialize the ETL Configuration plugin.
        Sets up Azure AI Search client for RAG functionality.
        """
        self.settings = get_settings()
        self._search_client: Optional[SearchClient] = None
        
        # Initialize Azure AI Search client
        try:
            if (hasattr(self.settings, 'azure_ai_search_endpoint') and 
                self.settings.azure_ai_search_endpoint and
                hasattr(self.settings, 'azure_ai_search_key') and
                self.settings.azure_ai_search_key and
                hasattr(self.settings, 'azure_ai_search_index_name') and
                self.settings.azure_ai_search_index_name):
                
                self._initialize_search_client()
                logger.info("✅ EtlConfigPlugin: Azure AI Search configured and ready")
            else:
                logger.warning("⚠️  EtlConfigPlugin: Azure AI Search not fully configured - will use fallback guidance")
        except Exception as e:
            logger.error(f"Error initializing EtlConfigPlugin: {str(e)}")
            logger.warning("⚠️  EtlConfigPlugin: Using fallback guidance")
        
        logger.info("EtlConfigPlugin initialized")
    
    def _initialize_search_client(self):
        """Initialize Azure AI Search client."""
        try:
            credential = AzureKeyCredential(self.settings.azure_ai_search_key)
            self._search_client = SearchClient(
                endpoint=self.settings.azure_ai_search_endpoint,
                index_name=self.settings.azure_ai_search_index_name,
                credential=credential
            )
            logger.info(f"Azure AI Search client initialized for index: {self.settings.azure_ai_search_index_name}")
        except Exception as e:
            logger.error(f"Failed to initialize Azure AI Search client: {str(e)}")
            self._search_client = None
    
    @kernel_function(
        description="Search ETL documentation for configuration guidance, examples, and best practices.",
        name="get_etl_documentation"
    )
    async def search_etl_documentation(self, user_request: str) -> str:
        """
        Search ETL documentation using RAG to provide relevant guidance.
        
        Args:
            user_request (str): User's question or request about ETL configuration
            
        Returns:
            str: Relevant documentation context and guidance
        """
        try:
            # ✅ HIGH PRIORITY VALIDATION I: Validate user_request is not empty
            if not user_request or not user_request.strip():
                error_msg = "Search request cannot be empty"
                logger.error(error_msg)
                return json.dumps({
                    "error": error_msg,
                    "suggestion": "Provide a specific question or topic about ETL configuration",
                    "examples": [
                        "How to configure Bronze layer ingestion?",
                        "What are the required parameters for SQL Server connection?",
                        "Best practices for Silver layer transformations",
                        "How to handle incremental data loading?"
                    ]
                }, indent=2)
            
            logger.info(f"🔍 EtlConfigPlugin: Searching ETL documentation for: {user_request}")
            
            # Try to search Azure AI Search if configured
            if self._search_client:
                try:
                    logger.info(f"Querying Azure AI Search index...")
                    # Perform semantic search with more results to capture fragmented information
                    results = self._search_client.search(
                        search_text=user_request,
                        query_type="semantic",
                        semantic_configuration_name="default",
                        top=5  # Increased from 3 to capture more context
                    )
                    
                    # Collect search results
                    search_results = []
                    for result in results:
                        search_results.append({
                            "section": result.get("section", ""),
                            "subsection": result.get("subsection", ""),
                            "content": result.get("content", ""),  # Return complete content (no truncation)
                            "content_type": result.get("content_type", "")
                        })
                    
                    if search_results:
                        logger.info(f"✅ Found {len(search_results)} relevant documentation chunks")
                        
                        # Format results for the LLM
                        formatted_response = "# ETL Configuration Documentation\n\n"
                        for i, result in enumerate(search_results, 1):
                            formatted_response += f"## Source {i}: {result['section']}"
                            if result['subsection']:
                                formatted_response += f" - {result['subsection']}"
                            formatted_response += "\n\n"
                            formatted_response += f"**Type**: {result['content_type']}\n\n"
                            formatted_response += f"{result['content']}\n\n"
                            formatted_response += "---\n\n"
                        
                        return formatted_response
                    else:
                        logger.warning("No results found in Azure AI Search, using fallback guidance")
                        return self._get_fallback_guidance(user_request)
                        
                except Exception as search_error:
                    logger.error(f"Error querying Azure AI Search: {str(search_error)}")
                    return self._get_fallback_guidance(user_request)
            else:
                logger.warning("Azure AI Search client not available, using fallback guidance")
                return self._get_fallback_guidance(user_request)
            
        except Exception as e:
            error_msg = f"Error searching ETL documentation: {str(e)}"
            logger.error(error_msg)
            return self._get_fallback_guidance(user_request)
    
    def _get_fallback_guidance(self, user_request: str) -> str:
        """
        Provide fallback guidance when search is not available or returns no results.
        
        Args:
            user_request (str): User's request
            
        Returns:
            str: Fallback guidance based on common ETL patterns
        """
        request_lower = user_request.lower()
        
        # Common ETL configuration guidance
        guidance_map = {
            "bronze": """Bronze Layer Configuration Guidance:
- Purpose: Raw data ingestion with minimal transformation
- Key parameters: source_connection, destination_path, file_format
- Best practices: Preserve original data structure, add ingestion metadata
- Common formats: Parquet, Delta Lake, JSON
- Example schema: Include _ingestion_date, _source_system fields""",
            
            "silver": """Silver Layer Configuration Guidance:
- Purpose: Cleaned and validated data with business rules applied
- Key parameters: transformation_rules, data_quality_checks, schema_mapping
- Best practices: Implement data validation, handle nulls, standardize formats
- Common transformations: Data type conversion, deduplication, field mapping
- Example schema: Standardized column names, consistent data types""",
            
            "gold": """Gold Layer Configuration Guidance:
- Purpose: Business-ready aggregated data for analytics
- Key parameters: aggregation_rules, business_logic, dimension_tables
- Best practices: Create fact and dimension tables, optimize for queries
- Common patterns: Star schema, slowly changing dimensions, calculated fields
- Example schema: Business-friendly naming, pre-calculated metrics""",
            
            "sql": """SQL Server Configuration Guidance:
- Connection parameters: server, database, authentication_type
- Security: Use Azure Key Vault for credentials, enable encryption
- Performance: Configure connection pooling, optimize batch sizes
- Example connection string format and required permissions""",
            
            "cosmos": """Cosmos DB Configuration Guidance:
- Connection parameters: endpoint, key, database_name, container_name
- Performance: Configure throughput, partition key strategy
- Best practices: Use appropriate consistency level, optimize queries
- Example document structure and indexing considerations""",
        }
        
        # Find relevant guidance
        for keyword, guidance in guidance_map.items():
            if keyword in request_lower:
                return f"ETL Configuration Guidance:\n\n{guidance}\n\nFor more specific guidance, please ensure Azure AI Search is configured with your documentation."
        
        # Generic guidance
        return """General ETL Configuration Guidance:

Common Configuration Structure:
- source: Define data source connection and parameters
- destination: Specify target location and format
- transformation: List data processing rules and logic
- metadata: Include pipeline metadata and lineage information

Key Considerations:
- Data Layer Strategy: Bronze (raw) → Silver (cleaned) → Gold (business-ready)
- Error Handling: Configure retry policies and error logging
- Performance: Set appropriate batch sizes and parallelism
- Security: Use secure credential management and data encryption

For detailed documentation and examples, please ensure Azure AI Search is configured with your ETL documentation."""
    
    @kernel_function(
        description="""Provides ETL configuration templates and examples for common scenarios:
        - Data layer templates (Bronze, Silver, Gold)
        - Source system connectors (SQL Server, APIs, Files)
        - Transformation patterns and examples
        - Best practice configurations
        """,
        name="get_config_template"
    )
    async def get_configuration_template(self, config_type: str) -> str:
        """
        Get ETL configuration templates for common scenarios.
        
        Args:
            config_type (str): Type of configuration template needed
            
        Returns:
            str: JSON template with explanatory comments
        """
        try:
            templates = {
                "bronze_sql": {
                    "description": "Bronze layer configuration for SQL Server ingestion",
                    "configuration": {
                        "pipeline_name": "bronze_sql_ingestion",
                        "layer": "bronze",
                        "source": {
                            "type": "sql_server",
                            "connection_string": "${SQL_CONNECTION_STRING}",
                            "query": "SELECT * FROM source_table",
                            "incremental_column": "modified_date"
                        },
                        "destination": {
                            "type": "delta_lake",
                            "path": "/bronze/domain/entity",
                            "format": "delta",
                            "mode": "append"
                        },
                        "metadata": {
                            "domain": "NielsenUS",
                            "entity": "sales_data",
                            "process_requested": "ingestion"
                        }
                    }
                },
                "silver_transformation": {
                    "description": "Silver layer transformation configuration",
                    "configuration": {
                        "pipeline_name": "silver_transformation",
                        "layer": "silver",
                        "source": {
                            "type": "delta_lake",
                            "path": "/bronze/domain/entity"
                        },
                        "transformations": [
                            {
                                "type": "data_quality",
                                "rules": ["remove_nulls", "validate_schema"]
                            },
                            {
                                "type": "standardization",
                                "rules": ["normalize_dates", "standardize_names"]
                            }
                        ],
                        "destination": {
                            "type": "delta_lake",
                            "path": "/silver/domain/entity",
                            "format": "delta"
                        }
                    }
                },
                "gold_aggregation": {
                    "description": "Gold layer aggregation configuration",
                    "configuration": {
                        "pipeline_name": "gold_aggregation",
                        "layer": "gold",
                        "source": {
                            "type": "delta_lake",
                            "path": "/silver/domain/entity"
                        },
                        "aggregations": [
                            {
                                "type": "group_by",
                                "columns": ["region", "product_category"],
                                "metrics": ["sum(sales)", "count(transactions)"]
                            }
                        ],
                        "destination": {
                            "type": "delta_lake",
                            "path": "/gold/domain/entity_summary"
                        }
                    }
                }
            }
            
            # Find matching template
            config_type_lower = config_type.lower()
            for template_key, template_data in templates.items():
                if template_key in config_type_lower or any(word in config_type_lower for word in template_key.split('_')):
                    return json.dumps(template_data, indent=2)
            
            # Return all templates if no specific match
            return json.dumps({"available_templates": templates}, indent=2)
            
        except Exception as e:
            logger.error(f"Error getting configuration template: {str(e)}")
            return json.dumps({"error": f"Failed to get template: {str(e)}"}, indent=2)
    
    async def cleanup(self):
        """
        Clean up resources used by the plugin.
        Should be called when the plugin is no longer needed.
        """
        try:
            if self._search_client:
                # Clean up search client resources
                pass
            logger.info("EtlConfigPlugin cleanup completed")
        except Exception as e:
            logger.error(f"Error during EtlConfigPlugin cleanup: {str(e)}")