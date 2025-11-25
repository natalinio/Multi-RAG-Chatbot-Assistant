"""
Test RAG end-to-end with extended documentation and JSON examples
"""

import asyncio
import sys
import os
from pathlib import Path

# Add parent dir to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.core.kernel_factory import get_kernel
from semantic_kernel.contents import ChatHistory
from semantic_kernel.connectors.ai.open_ai import AzureChatPromptExecutionSettings
from semantic_kernel.connectors.ai.function_choice_behavior import FunctionChoiceBehavior
from dotenv import load_dotenv

load_dotenv()


async def test_rag_with_extended_docs():
    """Test RAG with new extended documentation and JSON examples"""
    
    print("\n" + "="*80)
    print("RAG END-TO-END TEST WITH EXTENDED DOCUMENTATION")
    print("="*80)
    
    # Get kernel from factory
    kernel = await get_kernel()
    
    print("\n✓ Kernel initialized")
    print(f"  Plugins: {list(kernel.plugins.keys())}")
    
    # Get execution settings with function calling enabled
    execution_settings = AzureChatPromptExecutionSettings(
        max_tokens=2000,
        temperature=0.7,
        function_choice_behavior=FunctionChoiceBehavior.Auto()
    )
    
    # Get chat service
    chat_service = kernel.get_service("azure_openai_chat")
    
    # Test queries
    test_queries = [
        "Give me the exact JSON template for configuring an ingestion from SAPBW with a Bronze layer. Include all required fields.",
        "What is the structure of a Silver layer transformation process? Show the complete JSON template with explanations.",
        "How do I configure a data transformation from Bronze to Silver layer? Show a complete example.",
        "Show me all the different configuration examples available for SAPBW domain.",
        "What layers and process types are available in the system? List them all.",
    ]
    
    for query_idx, user_query in enumerate(test_queries, 1):
        print(f"\n{'-'*80}")
        print(f"TEST QUERY {query_idx}: {user_query[:70]}...")
        print(f"{'-'*80}")
        
        # Create chat history
        chat_history = ChatHistory()
        chat_history.add_system_message("""You are an ETL Assistant. When users ask about configuration templates or documentation:
1. Call the get_etl_documentation function IMMEDIATELY
2. Wait for retrieval results
3. Use ONLY the retrieved documentation to answer
4. Show exact JSON structures from documentation
5. If documentation doesn't fully answer, say so explicitly

Your goal is to provide factually accurate information from the documentation, not hallucinated content.""")
        
        # Add user message
        chat_history.add_user_message(user_query)
        
        # Invoke kernel
        try:
            response = await chat_service.get_chat_message_content(
                chat_history=chat_history,
                settings=execution_settings,
                kernel=kernel
            )
            
            response_text = str(response)
            
            # Analyze response
            print("\n✓ Response received:")
            print("-" * 80)
            print(response_text[:1000])
            if len(response_text) > 1000:
                print(f"\n... [Response continues, {len(response_text)} total chars]")
            print("-" * 80)
            
            # Check if RAG was likely used
            if any(keyword in response_text for keyword in ["JSON", "template", "configuration", "domain", "layer", "process"]):
                print("\n✓ Response appears to reference actual documentation/configurations")
            
        except Exception as e:
            print(f"\n✗ Error during query: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "="*80)
    print("✅ RAG END-TO-END TEST COMPLETED")
    print("="*80)


async def main():
    """Main entry point"""
    try:
        await test_rag_with_extended_docs()
    except Exception as e:
        print(f"\nFatal error: {e}")
        import traceback
        traceback.print_exc()
        exit(1)


if __name__ == "__main__":
    asyncio.run(main())
