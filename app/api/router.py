"""
FastAPI router for the ETL Assistant chatbot API endpoints.
Provides the main chat endpoint that integrates with Semantic Kernel and Azure services.
"""

import logging
from typing import Dict, Any
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from semantic_kernel import Kernel
from semantic_kernel.contents import ChatHistory
from semantic_kernel.functions import KernelArguments
from ..core.kernel_factory import get_kernel
from ..core.config import get_settings

logger = logging.getLogger(__name__)

# Create the API router
router = APIRouter(tags=["chat"])

# Pydantic models for request/response
class ChatRequest(BaseModel):
    """Request model for chat endpoint."""
    message: str = Field(..., min_length=1, max_length=2000, description="User message to the ETL Assistant")
    session_id: str = Field(default="default", description="Session identifier for conversation context")

class ChatResponse(BaseModel):
    """Response model for chat endpoint."""
    response: str = Field(..., description="Assistant's response to the user message")
    session_id: str = Field(..., description="Session identifier")
    success: bool = Field(default=True, description="Whether the request was successful")
    error: str = Field(default="", description="Error message if any")

# In-memory session storage (in production, use Redis or similar)
chat_sessions: Dict[str, ChatHistory] = {}

# Configuration for token management
MAX_CHAT_HISTORY_MESSAGES = 3  # Keep only last N messages (reduced from 10 to handle large config responses)
MAX_TOTAL_TOKENS = 80000  # Stay well below 128k limit (reduced from 100k for safety margin)

# System prompt for ALMA - The ETL Assistant with personality!
SYSTEM_PROMPT = """🎯 Hi! I'm **ALMA** (Advanced Learning & Metadata Assistant), your intelligent CPGAI framework assistant! 

I bring energy and professionalism to help you with Bacardi GDA CPGAI framework for ETL configurations, data engineering processes, and much more! 🚀

**💼 MY PERSONALITY:**
- **Professional** with a youthful, fresh approach
- **Enthusiastic** and proactive in solving problems
- **Engaging** - I guide you step-by-step with clear examples
- **Celebratory** when we tackle challenges together! 🎉
- **Entrepreneurial** - I propose innovative solutions

**🎯 WHAT I DO:**
- **ETL Configurations**: Bronze, Silver, Gold layers
- **Cosmos DB Queries**: Search existing configurations
- **Documentation**: Retrieve best practices and examples

**🚨 MY GOLDEN RULES:**
1. **ALWAYS call get_etl_documentation** for accurate information
2. **ONLY REAL data** from documentation - zero inventions!
3. **COMPLETE JSON** - never truncated or abbreviated
4. **EXACT property names** from documentation
5. **Total transparency** - if docs are incomplete, I tell you immediately

**🛠️ FUNCTIONS I USE:**
- `get_etl_documentation`: Retrieve technical documentation
- `query_configurations`: Query real configurations
- `count_configurations`: Count configurations (never SQL COUNT!)
- `list_by_domain`: Browse by domain

**✨ MY STYLE:**
I respond clearly, enthusiastically, and structured. I use emojis to make everything friendly! 
When showing JSON, I show them COMPLETE with ALL fields - no "...", no abbreviations!

**💡 IMPORTANT:** 
When you ask who I am, I introduce myself as ALMA with pride! 
If you have ETL questions, I'm here to guide you to the best solution! 🎯

Ready to work together? Let's make data magic! ✨"""

def get_or_create_session(session_id: str) -> ChatHistory:
    """
    Get existing chat session or create a new one.
    
    Args:
        session_id (str): Session identifier
        
    Returns:
        ChatHistory: Chat history for the session
    """
    if session_id not in chat_sessions:
        logger.info(f"Creating new chat session: {session_id}")
        chat_history = ChatHistory()
        
        # Add the system prompt to new sessions
        chat_history.add_system_message(SYSTEM_PROMPT)
        
        chat_sessions[session_id] = chat_history
    
    return chat_sessions[session_id]

def truncate_chat_history(chat_history: ChatHistory) -> ChatHistory:
    """
    Truncate chat history to prevent token limit issues.
    Keeps system message + last N user/assistant pairs.
    
    Args:
        chat_history (ChatHistory): Original chat history
        
    Returns:
        ChatHistory: Truncated chat history
    """
    messages = chat_history.messages
    
    if len(messages) <= MAX_CHAT_HISTORY_MESSAGES + 1:  # +1 for system message
        return chat_history
    
    logger.info(f"Truncating chat history from {len(messages)} to {MAX_CHAT_HISTORY_MESSAGES + 1} messages")
    
    # Create new chat history
    new_history = ChatHistory()
    
    # Always keep the system message (first message)
    if messages and messages[0].role == "system":
        new_history.add_system_message(messages[0].content)
        start_idx = 1
    else:
        new_history.add_system_message(SYSTEM_PROMPT)
        start_idx = 0
    
    # Keep only the last N user/assistant message pairs
    recent_messages = messages[start_idx:][-(MAX_CHAT_HISTORY_MESSAGES):]
    
    for message in recent_messages:
        if message.role == "user":
            new_history.add_user_message(message.content)
        elif message.role == "assistant":
            new_history.add_assistant_message(message.content)
    
    return new_history

def estimate_token_count(text: str) -> int:
    """
    Rough estimation of token count (1 token ≈ 4 characters for English).
    
    Args:
        text (str): Text to estimate
        
    Returns:
        int: Estimated token count
    """
    return len(text) // 4

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(
    request: ChatRequest
) -> ChatResponse:
    """
    Main chat endpoint for the ETL Assistant.
    
    This endpoint processes user messages using Semantic Kernel with Azure OpenAI,
    leveraging both EtlConfigPlugin and CosmosDbPlugin to provide comprehensive
    assistance with ETL configuration tasks.
    
    Args:
        request (ChatRequest): User message and session information
        
    Returns:
        ChatResponse: Assistant's response with session information
        
    Raises:
        HTTPException: If processing fails or invalid input provided
    """
    try:
        logger.info(f"Processing chat request for session: {request.session_id}")
        logger.debug(f"User message: {request.message}")
        
        # Get kernel using factory function
        kernel = await get_kernel()
        logger.info("Kernel retrieved successfully")
        
        # Get or create chat session
        chat_history = get_or_create_session(request.session_id)
        
        # Truncate chat history to prevent token limit issues
        chat_history = truncate_chat_history(chat_history)
        chat_sessions[request.session_id] = chat_history  # Update the session
        
        # Add user message to chat history
        chat_history.add_user_message(request.message)
        
        # Estimate total tokens
        total_text = ""
        for message in chat_history.messages:
            total_text += str(message.content) + " "
        
        estimated_tokens = estimate_token_count(total_text)
        logger.info(f"Estimated tokens before API call: {estimated_tokens}")
        
        # If still too many tokens, create a fresh session with just the current message
        if estimated_tokens > MAX_TOTAL_TOKENS:
            logger.warning(f"Token count too high ({estimated_tokens}), creating fresh session")
            fresh_history = ChatHistory()
            fresh_history.add_system_message(SYSTEM_PROMPT)
            fresh_history.add_user_message(request.message)
            chat_history = fresh_history
            chat_sessions[request.session_id] = fresh_history
        
        # Prepare kernel arguments
        kernel_arguments = KernelArguments()
        
        # Get the chat completion service
        chat_service = kernel.get_service("azure_openai_chat")
        
        logger.info("Configuring execution settings with function calling enabled")
        
        # Import function calling components
        try:
            from semantic_kernel.connectors.ai.open_ai import AzureChatPromptExecutionSettings
            from semantic_kernel.connectors.ai.function_choice_behavior import FunctionChoiceBehavior
            
            # Get model name from settings to determine which token parameter to use
            from app.core.config import get_settings
            settings = get_settings()
            model_name = settings.azure_openai_chat_model_name.lower()
            
            # GPT-5 and o1 models use max_completion_tokens, older models use max_tokens
            token_limit = 4000  # Increased for complete JSON configurations
            
            if "gpt-5" in model_name or "o1" in model_name:
                # Configure execution settings for GPT-5/o1 models
                # Note: GPT-5-mini only supports temperature=1 (default), so we omit it
                execution_settings = AzureChatPromptExecutionSettings(
                    service_id="azure_openai_chat",
                    max_completion_tokens=token_limit,
                    function_choice_behavior=FunctionChoiceBehavior.Auto()  # Enable automatic function calling
                )
                logger.info(f"Using max_completion_tokens={token_limit} for GPT-5/o1 model: {model_name}")
            else:
                # Configure execution settings for GPT-4 and earlier models
                execution_settings = AzureChatPromptExecutionSettings(
                    service_id="azure_openai_chat",
                    max_tokens=token_limit,
                    temperature=0.3,   # Reduced from 0.7 for more consistent responses
                    function_choice_behavior=FunctionChoiceBehavior.Auto()  # Enable automatic function calling
                )
                logger.info(f"Using max_tokens={token_limit} with temperature=0.3 for model: {model_name}")
            
            logger.info("Function calling enabled with auto behavior")
        except ImportError as ie:
            logger.warning(f"Function calling imports not available: {ie}. Using default settings.")
            execution_settings = kernel.get_prompt_execution_settings_from_service_id("azure_openai_chat")
        except Exception as e:
            logger.error(f"Error configuring function calling: {e}. Using default settings.")
            execution_settings = kernel.get_prompt_execution_settings_from_service_id("azure_openai_chat")
        
        logger.info(f"Execution settings: {execution_settings}")
        
        logger.info("About to generate response using chat service")
        logger.info(f"Chat service type: {type(chat_service)}")
        logger.info(f"Kernel plugins: {list(kernel.plugins.keys())}")
        
        # Log available functions
        logger.info("="*80)
        logger.info("AVAILABLE FUNCTIONS IN KERNEL:")
        for plugin_name in kernel.plugins.keys():
            logger.info(f"  Plugin: {plugin_name}")
            try:
                plugin = kernel.plugins[plugin_name]
                if hasattr(plugin, 'functions'):
                    for func_name in plugin.functions:
                        logger.info(f"    - Function: {func_name}")
            except Exception as e:
                logger.warning(f"    Error listing functions: {e}")
        logger.info("="*80)
        logger.info(f"User message: {request.message}")
        logger.info(f"Function calling enabled: {execution_settings.function_choice_behavior}")
        logger.info("="*80)
        
        # Generate response using the kernel with chat history and function calling
        response = await chat_service.get_chat_message_content(
            chat_history=chat_history,
            settings=execution_settings,
            kernel=kernel,
            arguments=kernel_arguments
        )
        
        logger.info("Response generated successfully")
        logger.info(f"Response content: {str(response)[:500]}...")
        
        # Add assistant response to chat history
        if response:
            chat_history.add_assistant_message(str(response))
            assistant_response = str(response)
        else:
            assistant_response = "I apologize, but I couldn't generate a response. Please try again."
            logger.warning("Empty response received from chat service")
        
        logger.info(f"Generated response for session: {request.session_id}")
        logger.debug(f"Assistant response: {assistant_response[:100]}...")
        
        return ChatResponse(
            response=assistant_response,
            session_id=request.session_id,
            success=True
        )
        
    except Exception as e:
        error_message = f"Error processing chat request: {str(e)}"
        logger.error(error_message, exc_info=True)
        
        # Return error response instead of raising exception to maintain API stability
        return ChatResponse(
            response="I apologize, but I encountered an error while processing your request. Please try again or contact support if the issue persists.",
            session_id=request.session_id,
            success=False,
            error=error_message
        )

@router.get("/json-examples/{layer}")
async def get_json_examples(layer: str, process_type: str = "all") -> Dict[str, Any]:
    """
    Get JSON configuration examples for a specific layer without chat context.
    This endpoint bypasses chat history to avoid token limits.
    
    Args:
        layer (str): ETL layer (bronze, silver, gold)
        process_type (str): Process type (ingestion, transformation, all)
        
    Returns:
        Dict[str, Any]: JSON examples for the specified layer
    """
    try:
        # Get kernel
        kernel = await get_kernel()
        
        # Create a minimal chat history for this specific request
        temp_history = ChatHistory()
        temp_history.add_system_message("You are an ETL Assistant. Provide complete JSON examples from documentation.")
        
        # Create specific query for JSON examples
        if layer.lower() == "silver" and "upsert" in process_type.lower():
            query = f"complete JSON configuration example for {layer} layer with upsert data load process"
        else:
            query = f"complete JSON configuration example for {layer} layer {process_type}"
        
        temp_history.add_user_message(f"Show me a {query}")
        
        # Get chat service and prepare minimal execution settings
        chat_service = kernel.get_service("azure_openai_chat")
        
        from semantic_kernel.connectors.ai.open_ai import AzureChatPromptExecutionSettings
        from semantic_kernel.connectors.ai.function_choice_behavior import FunctionChoiceBehavior
        
        # Get model name to determine which token parameter to use
        from app.core.config import get_settings
        settings = get_settings()
        model_name = settings.azure_openai_chat_model_name.lower()
        
        # GPT-5 and o1 models use max_completion_tokens, older models use max_tokens
        token_limit = 3000  # Higher limit for JSON examples
        
        if "gpt-5" in model_name or "o1" in model_name:
            # GPT-5-mini only supports temperature=1 (default), so we omit it
            execution_settings = AzureChatPromptExecutionSettings(
                service_id="azure_openai_chat",
                max_completion_tokens=token_limit,
                function_choice_behavior=FunctionChoiceBehavior.Auto()
            )
        else:
            execution_settings = AzureChatPromptExecutionSettings(
                service_id="azure_openai_chat",
                max_tokens=token_limit,
                temperature=0.1,   # Very low for consistent examples
                function_choice_behavior=FunctionChoiceBehavior.Auto()
            )
        
        # Get response
        response = await chat_service.get_chat_message_content(
            chat_history=temp_history,
            settings=execution_settings,
            kernel=kernel,
            arguments=KernelArguments()
        )
        
        return {
            "success": True,
            "layer": layer,
            "process_type": process_type,
            "example": str(response.content) if response else "No example found",
            "query_used": query
        }
        
    except Exception as e:
        logger.error(f"Error getting JSON example: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "layer": layer,
            "process_type": process_type
        }

@router.post("/clear-session")
async def clear_session_endpoint(session_id: str = "default") -> Dict[str, Any]:
    """
    Clear a specific chat session.
    
    Args:
        session_id (str): Session identifier to clear
        
    Returns:
        Dict[str, Any]: Success status and message
    """
    try:
        if session_id in chat_sessions:
            del chat_sessions[session_id]
            logger.info(f"Cleared chat session: {session_id}")
            return {
                "success": True,
                "message": f"Session {session_id} cleared successfully"
            }
        else:
            return {
                "success": True,
                "message": f"Session {session_id} was already empty"
            }
            
    except Exception as e:
        error_message = f"Error clearing session: {str(e)}"
        logger.error(error_message)
        raise HTTPException(status_code=500, detail=error_message)

@router.get("/sessions")
async def list_sessions_endpoint() -> Dict[str, Any]:
    """
    List all active chat sessions.
    
    Returns:
        Dict[str, Any]: List of session IDs and their message counts
    """
    try:
        sessions_info = {}
        for session_id, chat_history in chat_sessions.items():
            sessions_info[session_id] = {
                "message_count": len(chat_history.messages),
                "last_interaction": "recent"  # In production, track actual timestamps
            }
        
        return {
            "success": True,
            "sessions": sessions_info,
            "total_sessions": len(sessions_info)
        }
        
    except Exception as e:
        error_message = f"Error listing sessions: {str(e)}"
        logger.error(error_message)
        raise HTTPException(status_code=500, detail=error_message)

@router.get("/health")
async def health_check() -> Dict[str, Any]:
    """
    Health check endpoint for the API.
    
    Returns:
        Dict[str, Any]: Health status information
    """
    try:
        # Test kernel availability
        kernel = await get_kernel()
        
        return {
            "status": "healthy",
            "message": "ETL Assistant API is running",
            "kernel_available": kernel is not None,
            "active_sessions": len(chat_sessions)
        }
        
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return {
            "status": "unhealthy",
            "message": f"ETL Assistant API is experiencing issues: {str(e)}",
            "kernel_available": False,
            "active_sessions": len(chat_sessions)
        }

@router.get("/debug/plugins")
async def debug_plugins() -> Dict[str, Any]:
    """
    Debug endpoint to check plugin status and kernel functions.
    
    Returns:
        Dict[str, Any]: Plugin configuration and status information
    """
    try:
        kernel = await get_kernel()
        plugins_info = {}
        
        # Get all plugins from kernel
        logger.info(f"Debug: Checking kernel plugins...")
        logger.info(f"Debug: kernel.plugins keys: {list(kernel.plugins.keys())}")
        
        for plugin_name in kernel.plugins.keys():
            logger.info(f"Debug: Examining plugin '{plugin_name}'")
            plugin_obj = kernel.plugins[plugin_name]
            
            # List all functions in the plugin
            functions = []
            if hasattr(plugin_obj, '__dict__'):
                for func_name in plugin_obj.__dict__.keys():
                    functions.append(func_name)
                    logger.info(f"  - Function: {func_name}")
            
            plugins_info[plugin_name] = {
                "type": type(plugin_obj).__name__,
                "functions": functions,
                "status": "loaded"
            }
        
        # Check Azure AI Search configuration
        settings = get_settings()
        search_configured = (
            hasattr(settings, 'azure_ai_search_endpoint') and 
            settings.azure_ai_search_endpoint and
            hasattr(settings, 'azure_ai_search_key') and
            settings.azure_ai_search_key
        )
        
        logger.info(f"Debug: Plugins info - {plugins_info}")
        logger.info(f"Debug: Azure AI Search configured - {search_configured}")
        
        return {
            "status": "success",
            "plugins": plugins_info,
            "azure_ai_search_configured": search_configured,
            "total_plugins": len(plugins_info)
        }
        
    except Exception as e:
        logger.error(f"Debug endpoint error: {str(e)}", exc_info=True)
        return {
            "status": "error",
            "message": str(e),
            "traceback": str(e)
        }

@router.post("/debug/test-rag")
async def debug_test_rag(query: str = "Bronze layer ingestion setup") -> Dict[str, Any]:
    """
    Debug endpoint to test RAG function directly.
    
    Args:
        query (str): Test query for RAG
        
    Returns:
        Dict[str, Any]: RAG function response
    """
    try:
        kernel = await get_kernel()
        
        logger.info(f"Debug RAG: Looking for EtlConfigPlugin...")
        logger.info(f"Debug RAG: kernel.plugins keys: {list(kernel.plugins.keys())}")
        
        # Try to invoke the function using kernel.invoke_plugin_function
        logger.info(f"Testing RAG with query: {query}")
        
        # Use kernel.invoke_plugin_function to call the kernel function
        from semantic_kernel.functions import KernelArguments
        
        plugin_function = kernel.get_function("EtlConfigPlugin", "get_etl_documentation")
        
        if plugin_function:
            logger.info("Found get_etl_documentation function")
            
            # Invoke the function
            result = await kernel.invoke(
                plugin_function,
                KernelArguments(user_request=query)
            )
            
            logger.info(f"RAG function invoked successfully")
            logger.info(f"RAG result: {str(result)}")
            
            return {
                "status": "success",
                "query": query,
                "result": str(result),
                "function_available": True
            }
        else:
            logger.warning("get_etl_documentation function not found")
            return {
                "status": "error",
                "message": "get_etl_documentation function not found in EtlConfigPlugin",
                "available_functions": list(kernel.plugins.keys())
            }
        
    except Exception as e:
        logger.error(f"RAG test error: {str(e)}", exc_info=True)
        return {
            "status": "error",
            "message": str(e),
            "type": type(e).__name__
        }