"""
Test script to verify that the RAG function is properly registered in the Semantic Kernel
and visible to the LLM for function calling.
"""

import asyncio
import json
import logging
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.connectors.ai.function_choice_behavior import FunctionChoiceBehavior
from semantic_kernel.connectors.ai.open_ai import AzureChatPromptExecutionSettings
from semantic_kernel.contents import ChatHistory
from semantic_kernel.functions import KernelArguments

# Setup
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

async def test_kernel_functions():
    """Test if kernel functions are properly registered for function calling."""
    
    print("\n" + "="*70)
    print("TESTING SEMANTIC KERNEL FUNCTION REGISTRATION")
    print("="*70 + "\n")
    
    from app.core.kernel_factory import get_kernel
    
    # Get kernel
    kernel = await get_kernel()
    
    print("📋 Kernel Plugins and Functions:\n")
    
    # List all plugins
    for plugin_name in kernel.plugins.keys():
        print(f"Plugin: {plugin_name}")
        plugin = kernel.plugins[plugin_name]
        
        # Try to find functions
        if hasattr(plugin, '__dict__'):
            methods = [m for m in dir(plugin) if not m.startswith('_') and callable(getattr(plugin, m))]
            print(f"  Methods: {methods}")
        
        # Get kernel functions - this is the correct way
        try:
            # List functions in this plugin
            functions = []
            for func_name in dir(plugin):
                if not func_name.startswith('_'):
                    func = getattr(plugin, func_name, None)
                    if callable(func) and hasattr(func, '__wrapped__'):
                        functions.append(func_name)
                        print(f"  ✅ Kernel Function: {func_name}")
            
            if not functions:
                print(f"  ⚠️  No kernel functions found (try looking at __call__ or _kernel_functions)")
        except Exception as e:
            print(f"  ❌ Error listing functions: {e}")
        
        print()
    
    # Now test function calling
    print("\n" + "="*70)
    print("TESTING FUNCTION CALLING WITH LLM")
    print("="*70 + "\n")
    
    # Create chat history
    chat_history = ChatHistory()
    chat_history.add_system_message("""You are an ETL Assistant. You have access to functions to search ETL documentation.
When a user asks about ETL configuration, template, JSON examples, or best practices, you MUST use the get_etl_documentation function.
Always use the available functions to retrieve documentation before answering.""")
    
    chat_history.add_user_message("Give me the template JSON to configure an ingestion from SAPBW")
    
    # Setup execution settings with function calling
    execution_settings = AzureChatPromptExecutionSettings(
        service_id="azure_openai_chat",
        max_tokens=2000,
        temperature=0.7,
        function_choice_behavior=FunctionChoiceBehavior.Auto()
    )
    
    # Get chat service
    chat_service = kernel.get_service("azure_openai_chat")
    
    print("Calling LLM with function calling enabled...\n")
    
    try:
        response = await chat_service.get_chat_message_content(
            chat_history=chat_history,
            settings=execution_settings,
            kernel=kernel,
            arguments=KernelArguments()
        )
        
        print("LLM Response:")
        print("-" * 70)
        print(str(response))
        print("-" * 70)
        
        # Check if it looks like it actually called the function
        response_str = str(response).lower()
        if "sapbw" in response_str or "sapcdc" in response_str or "template" in response_str:
            print("\n✅ Response contains expected content from documentation")
        else:
            print("\n⚠️  Response might be hallucinated - doesn't contain expected keywords")
            
    except Exception as e:
        print(f"❌ Error during function calling: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_kernel_functions())
