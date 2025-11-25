"""
Cosmos DB service for querying ETL configurations.
Implements async methods for connecting to and querying Azure Cosmos DB.
"""

import asyncio
import logging
from typing import List, Dict, Any, Optional
from azure.cosmos import CosmosClient, exceptions
from azure.cosmos.aio import CosmosClient as AsyncCosmosClient
from azure.cosmos.aio import DatabaseProxy, ContainerProxy
from ..core.config import get_settings

logger = logging.getLogger(__name__)


class CosmosService:
    """
    Service class for Azure Cosmos DB operations.
    Handles connection management and SQL query execution against the configurations container.
    """
    
    def __init__(self):
        """Initialize the Cosmos DB service with configuration settings."""
        self.settings = get_settings()
        self._client: Optional[AsyncCosmosClient] = None
        self._database: Optional[DatabaseProxy] = None
        self._container: Optional[ContainerProxy] = None
    
    async def _ensure_connection(self) -> None:
        """
        Ensure that the Cosmos DB connection is established.
        Creates client, database, and container references if not already created.
        """
        if self._client is None:
            try:
                # Initialize async Cosmos client
                self._client = AsyncCosmosClient(
                    url=self.settings.cosmos_db_endpoint,
                    credential=self.settings.cosmos_db_key
                )
                
                # Get database reference
                self._database = self._client.get_database_client(
                    self.settings.cosmos_db_database_name
                )
                
                # Get container reference
                self._container = self._database.get_container_client(
                    self.settings.cosmos_db_container_name
                )
                
                logger.info(f"Connected to Cosmos DB: {self.settings.cosmos_db_database_name}/{self.settings.cosmos_db_container_name}")
                
            except Exception as e:
                logger.error(f"Failed to connect to Cosmos DB: {str(e)}")
                raise
    
    async def query_configurations(self, sql_query: str) -> List[Dict[str, Any]]:
        """
        Execute a SQL query against the configurations container in Cosmos DB.
        
        Args:
            sql_query (str): SQL query string to execute against the container
            
        Returns:
            List[Dict[str, Any]]: List of configuration documents matching the query
            
        Raises:
            Exception: If query execution fails or connection issues occur
        """
        try:
            # Ensure connection is established
            await self._ensure_connection()
            
            if self._container is None:
                raise Exception("Cosmos DB container connection not established")
            
            logger.info(f"Executing query: {sql_query}")
            
            # Execute the SQL query
            items = []
            async for item in self._container.query_items(
                query=sql_query
            ):
                items.append(item)
            
            logger.info(f"Query returned {len(items)} items")
            return items
            
        except exceptions.CosmosHttpResponseError as e:
            error_msg = f"Cosmos DB HTTP error: {e.status_code} - {e.message}"
            logger.error(error_msg)
            raise Exception(error_msg)
            
        except exceptions.CosmosResourceNotFoundError as e:
            error_msg = f"Cosmos DB resource not found: {str(e)}"
            logger.error(error_msg)
            raise Exception(error_msg)
            
        except Exception as e:
            error_msg = f"Error executing Cosmos DB query: {str(e)}"
            logger.error(error_msg)
            raise Exception(error_msg)
    
    async def get_configuration_by_id(self, item_id: str, partition_key: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a specific configuration by its ID and partition key.
        
        Args:
            item_id (str): The ID of the configuration document
            partition_key (str): The partition key value
            
        Returns:
            Optional[Dict[str, Any]]: The configuration document if found, None otherwise
        """
        try:
            await self._ensure_connection()
            
            if self._container is None:
                raise Exception("Cosmos DB container connection not established")
            
            item = await self._container.read_item(
                item=item_id,
                partition_key=partition_key
            )
            
            logger.info(f"Retrieved configuration with ID: {item_id}")
            return item
            
        except exceptions.CosmosResourceNotFoundError:
            logger.warning(f"Configuration not found with ID: {item_id}")
            return None
            
        except Exception as e:
            error_msg = f"Error retrieving configuration by ID: {str(e)}"
            logger.error(error_msg)
            raise Exception(error_msg)
    
    async def list_configurations_by_domain(self, domain: str, limit: int = 100) -> List[Dict[str, Any]]:
        """
        List configurations filtered by domain with optional limit.
        
        Args:
            domain (str): The domain to filter by
            limit (int): Maximum number of results to return (default: 100)
            
        Returns:
            List[Dict[str, Any]]: List of configuration documents
        """
        sql_query = f"SELECT TOP {limit} * FROM c WHERE c.domain = @domain ORDER BY c._ts DESC"
        
        try:
            await self._ensure_connection()
            
            if self._container is None:
                raise Exception("Cosmos DB container connection not established")
            
            items = []
            async for item in self._container.query_items(
                query=sql_query,
                parameters=[{"name": "@domain", "value": domain}]
            ):
                items.append(item)
            
            logger.info(f"Retrieved {len(items)} configurations for domain: {domain}")
            return items
            
        except Exception as e:
            error_msg = f"Error listing configurations by domain: {str(e)}"
            logger.error(error_msg)
            raise Exception(error_msg)
    
    async def close(self) -> None:
        """Close the Cosmos DB client connection."""
        if self._client:
            await self._client.close()
            self._client = None
            self._database = None
            self._container = None
            logger.info("Cosmos DB connection closed")
    
    async def __aenter__(self):
        """Async context manager entry."""
        await self._ensure_connection()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close()