"""
Kernel Factory for Semantic Kernel initialization.
Configures and creates a Semantic Kernel instance with Azure OpenAI and plugins.
"""

import logging
from typing import Optional
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.connectors.ai.open_ai import AzureTextEmbedding
from semantic_kernel.core_plugins import ConversationSummaryPlugin, TextPlugin
from ..plugins.CosmosDbPlugin.CosmosDbPlugin import CosmosDbPlugin
from ..plugins.EtlConfigPlugin.EtlConfigPlugin import EtlConfigPlugin
from .config import get_settings

logger = logging.getLogger(__name__)


class KernelFactory:
    """
    Factory class for creating and configuring Semantic Kernel instances.
    
    This factory handles the initialization of:
    - Azure OpenAI services (chat completion and embeddings)
    - Custom plugins (CosmosDbPlugin and EtlConfigPlugin)
    - Core plugins for enhanced functionality
    """
    
    def __init__(self):
        """Initialize the kernel factory with settings."""
        self.settings = get_settings()
        self._kernel: Optional[Kernel] = None
        logger.info("KernelFactory initialized")
    
    async def create_kernel(self) -> Kernel:
        """
        Create and configure a new Semantic Kernel instance.
        
        Returns:
            Kernel: Configured Semantic Kernel instance with Azure OpenAI services and plugins
            
        Raises:
            Exception: If kernel creation or configuration fails
        """
        try:
            logger.info("Creating Semantic Kernel instance")
            
            # Initialize the kernel
            kernel = Kernel()
            
            # Configure Azure OpenAI Chat Completion service
            await self._configure_chat_completion(kernel)
            
            # Configure Azure OpenAI Text Embedding service
            await self._configure_text_embedding(kernel)
            
            # Add custom plugins
            await self._add_custom_plugins(kernel)
            
            # Add core plugins for enhanced functionality
            await self._add_core_plugins(kernel)
            
            self._kernel = kernel
            logger.info("Semantic Kernel created and configured successfully")
            
            return kernel
            
        except Exception as e:
            error_msg = f"Failed to create Semantic Kernel: {str(e)}"
            logger.error(error_msg)
            raise Exception(error_msg)
    
    async def _configure_chat_completion(self, kernel: Kernel) -> None:
        """
        Configure Azure OpenAI Chat Completion service with function calling enabled.
        
        Args:
            kernel (Kernel): The kernel instance to configure
        """
        try:
            logger.info("Configuring Azure OpenAI Chat Completion service")
            
            # Create Azure OpenAI Chat Completion service
            chat_completion = AzureChatCompletion(
                deployment_name=self.settings.azure_openai_chat_model_name,
                endpoint=self.settings.azure_openai_endpoint,
                api_key=self.settings.azure_openai_api_key,
                api_version=self.settings.azure_openai_api_version,
                service_id="azure_openai_chat"
            )
            
            # Add the service to the kernel
            kernel.add_service(chat_completion)
            
            logger.info(f"Azure OpenAI Chat Completion configured with model: {self.settings.azure_openai_chat_model_name}")
            logger.info("Function calling capabilities enabled for automatic plugin invocation")
            
        except Exception as e:
            error_msg = f"Failed to configure Azure OpenAI Chat Completion: {str(e)}"
            logger.error(error_msg)
            raise Exception(error_msg)
    
    async def _configure_text_embedding(self, kernel: Kernel) -> None:
        """
        Configure Azure OpenAI Text Embedding service.
        
        Args:
            kernel (Kernel): The kernel instance to configure
        """
        try:
            logger.info("Configuring Azure OpenAI Text Embedding service")
            
            # Create Azure OpenAI Text Embedding service
            text_embedding = AzureTextEmbedding(
                deployment_name=self.settings.azure_openai_embedding_model_name,
                endpoint=self.settings.azure_openai_endpoint,
                api_key=self.settings.azure_openai_api_key,
                api_version=self.settings.azure_openai_api_version,
                service_id="azure_openai_embedding"
            )
            
            # Add the service to the kernel
            kernel.add_service(text_embedding)
            
            logger.info(f"Azure OpenAI Text Embedding configured with model: {self.settings.azure_openai_embedding_model_name}")
            
        except Exception as e:
            error_msg = f"Failed to configure Azure OpenAI Text Embedding: {str(e)}"
            logger.error(error_msg)
            raise Exception(error_msg)
    
    async def _add_custom_plugins(self, kernel: Kernel) -> None:
        """
        Add custom plugins to the kernel.
        
        Args:
            kernel (Kernel): The kernel instance to configure
        """
        try:
            logger.info("Adding custom plugins to kernel")
            
            # Add CosmosDbPlugin for querying existing configurations
            cosmos_plugin = CosmosDbPlugin()
            kernel.add_plugin(cosmos_plugin, plugin_name="CosmosDbPlugin")
            logger.info("CosmosDbPlugin added successfully")
            
            # Add EtlConfigPlugin for RAG-based ETL configuration assistance
            etl_config_plugin = EtlConfigPlugin()
            kernel.add_plugin(etl_config_plugin, plugin_name="EtlConfigPlugin")
            logger.info("EtlConfigPlugin added successfully")
            
            logger.info("All custom plugins added successfully")
            
        except Exception as e:
            error_msg = f"Failed to add custom plugins: {str(e)}"
            logger.error(error_msg)
            raise Exception(error_msg)
    
    async def _add_core_plugins(self, kernel: Kernel) -> None:
        """
        Add core Semantic Kernel plugins for enhanced functionality.
        
        Args:
            kernel (Kernel): The kernel instance to configure
        """
        try:
            logger.info("Adding core plugins to kernel")
            
            # Note: ConversationSummaryPlugin temporarily disabled due to version compatibility
            # TODO: Fix ConversationSummaryPlugin initialization for current SK version
            # conversation_plugin = ConversationSummaryPlugin()
            # kernel.add_plugin(conversation_plugin, plugin_name="ConversationSummaryPlugin")
            # logger.info("ConversationSummaryPlugin added successfully")
            
            # Add TextPlugin for text manipulation utilities
            text_plugin = TextPlugin()
            kernel.add_plugin(text_plugin, plugin_name="TextPlugin")
            logger.info("TextPlugin added successfully")
            
            logger.info("All core plugins added successfully")
            
        except Exception as e:
            error_msg = f"Failed to add core plugins: {str(e)}"
            logger.error(error_msg)
            raise Exception(error_msg)
    
    async def get_kernel(self) -> Kernel:
        """
        Get the current kernel instance or create a new one if none exists.
        
        Returns:
            Kernel: The configured Semantic Kernel instance
        """
        if self._kernel is None:
            self._kernel = await self.create_kernel()
        
        return self._kernel
    
    async def reset_kernel(self) -> Kernel:
        """
        Reset and recreate the kernel instance.
        
        Returns:
            Kernel: New configured Semantic Kernel instance
        """
        logger.info("Resetting kernel instance")
        
        # Clean up existing kernel if any
        if self._kernel is not None:
            await self._cleanup_kernel()
        
        # Create new kernel
        self._kernel = await self.create_kernel()
        return self._kernel
    
    async def _cleanup_kernel(self) -> None:
        """
        Clean up resources used by the current kernel.
        """
        try:
            if self._kernel is not None:
                # Clean up custom plugins if they have cleanup methods
                cosmos_plugin = self._kernel.get_plugin("CosmosDbPlugin")
                if cosmos_plugin and hasattr(cosmos_plugin, 'cleanup'):
                    await cosmos_plugin.cleanup()
                
                etl_plugin = self._kernel.get_plugin("EtlConfigPlugin")
                if etl_plugin and hasattr(etl_plugin, 'cleanup'):
                    await etl_plugin.cleanup()
                
                self._kernel = None
                logger.info("Kernel cleanup completed")
                
        except Exception as e:
            logger.error(f"Error during kernel cleanup: {str(e)}")
    
    async def cleanup(self) -> None:
        """
        Cleanup method to be called when the factory is no longer needed.
        """
        await self._cleanup_kernel()
        logger.info("KernelFactory cleanup completed")


# Global kernel factory instance
_kernel_factory: Optional[KernelFactory] = None


async def get_kernel_factory() -> KernelFactory:
    """
    Get the global kernel factory instance.
    
    Returns:
        KernelFactory: Global kernel factory instance
    """
    global _kernel_factory
    
    if _kernel_factory is None:
        _kernel_factory = KernelFactory()
    
    return _kernel_factory


async def get_kernel() -> Kernel:
    """
    Get a configured Semantic Kernel instance.
    
    Returns:
        Kernel: Configured Semantic Kernel instance
    """
    factory = await get_kernel_factory()
    return await factory.get_kernel()


async def reset_kernel() -> Kernel:
    """
    Reset and get a new Semantic Kernel instance.
    
    Returns:
        Kernel: New configured Semantic Kernel instance
    """
    factory = await get_kernel_factory()
    return await factory.reset_kernel()