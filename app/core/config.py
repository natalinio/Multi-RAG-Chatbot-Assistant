"""
Configuration management using Pydantic Settings.
Loads environment variables and provides typed configuration access.
"""

from typing import List, Optional
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    # Azure OpenAI Configuration
    azure_openai_api_key: str = Field(..., description="Azure OpenAI API key")
    azure_openai_endpoint: str = Field(..., description="Azure OpenAI endpoint URL")
    azure_openai_chat_model_name: str = Field(..., description="Azure OpenAI chat model deployment name")
    azure_openai_embedding_model_name: str = Field(..., description="Azure OpenAI embedding model deployment name")
    azure_openai_api_version: str = Field(default="2024-12-01-preview", description="Azure OpenAI API version")
    
    # Azure Cosmos DB Configuration
    cosmos_db_endpoint: str = Field(..., description="Azure Cosmos DB endpoint URL")
    cosmos_db_key: str = Field(..., description="Azure Cosmos DB primary key")
    cosmos_db_database_name: str = Field(..., description="Cosmos DB database name")
    cosmos_db_container_name: str = Field(..., description="Cosmos DB container name")
    
    # Azure AI Search Configuration (for RAG)
    azure_ai_search_endpoint: str = Field(..., description="Azure AI Search endpoint URL")
    azure_ai_search_key: str = Field(..., description="Azure AI Search API key")
    azure_ai_search_index_name: str = Field(default="cpgai-gda-version", description="Azure AI Search index name")
    
    # Application Configuration
    environment: str = Field(default="development", description="Application environment")
    log_level: str = Field(default="INFO", description="Logging level")
    cors_origins: str = Field(
        default="http://localhost:3000,http://127.0.0.1:3000",
        description="CORS allowed origins (comma-separated)"
    )
    
    # FastAPI Configuration
    app_title: str = Field(default="ETL Config & Cosmos DB Q&A Chatbot", description="Application title")
    app_description: str = Field(
        default="A chatbot that answers questions about ETL configurations and queries Cosmos DB data",
        description="Application description"
    )
    app_version: str = Field(default="1.0.0", description="Application version")
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Convert CORS_ORIGINS string to list if needed."""
        if isinstance(self.cors_origins, str):
            return [origin.strip() for origin in self.cors_origins.split(",")]
        return self.cors_origins
    
    @property
    def is_development(self) -> bool:
        """Check if running in development environment."""
        return self.environment.lower() == "development"
    
    @property
    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.environment.lower() == "production"


# Global settings instance
_settings: Optional[Settings] = None


def get_settings() -> Settings:
    """
    Get the global settings instance.
    Creates a new instance if one doesn't exist.
    
    Returns:
        Settings: Application settings instance
    """
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings