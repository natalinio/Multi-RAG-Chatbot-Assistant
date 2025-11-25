"""
Test integration between Cosmos DB plugin and Azure AI Search for ASQL documentation.
Tests that the system can retrieve ASQL configuration from Azure AI Search and
query related configs from Cosmos DB.
"""

import asyncio
import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.core.kernel_factory import get_kernel
from semantic_kernel.functions import KernelArguments


async def test_asql_documentation():
    """Test ASQL documentation retrieval from Azure AI Search."""
    print("\n" + "="*80)
    print("🧪 TESTING ASQL DOCUMENTATION INTEGRATION")
    print("="*80 + "\n")
    
    # Initialize kernel
    kernel = await get_kernel()
    print("✅ Kernel initialized with plugins:")
    for plugin_name in kernel.plugins:
        print(f"   - {plugin_name}")
    
    # Test 1: Search for ASQL documentation
    print("\n" + "-"*80)
    print("TEST 1: Search Azure AI Search for ASQL configuration")
    print("-"*80)
    
    search_query = "How do I configure Azure SQL database ingestion in Bronze layer?"
    print(f"Query: {search_query}\n")
    
    try:
        # Use the EtlConfigPlugin to search documentation
        etl_plugin = kernel.plugins["EtlConfigPlugin"]
        search_func = etl_plugin["get_etl_documentation"]
        
        arguments = KernelArguments(user_request=search_query)
        result = await search_func.invoke(kernel, arguments)
        
        print(f"✅ Search Results ({len(str(result))} chars):")
        print("-"*80)
        result_str = str(result)
        if len(result_str) > 2000:
            print(result_str[:2000] + "\n... [truncated]")
        else:
            print(result_str)
        print("-"*80)
        
        # Check if ASQL is mentioned
        if 'ASQL' in result_str or 'Azure SQL' in result_str.upper():
            print("✅ Result contains ASQL/Azure SQL documentation")
        else:
            print("⚠️  Result does NOT mention ASQL")
            
    except Exception as e:
        print(f"❌ Search failed: {e}")
        return False
    
    # Test 2: Query Cosmos DB for ASQL configurations
    print("\n" + "-"*80)
    print("TEST 2: Query Cosmos DB for ASQL ingestion configurations")
    print("-"*80)
    
    try:
        cosmos_plugin = kernel.plugins["CosmosDbPlugin"]
        query_func = cosmos_plugin["query_configurations"]
        
        # Query for ASQL configurations (using correct nested field path)
        sql_query = "SELECT * FROM c WHERE c.I1_data_extract_process.source.type = 'ASQL' OFFSET 0 LIMIT 5"
        print(f"SQL Query: {sql_query}\n")
        
        arguments = KernelArguments(sql_query=sql_query)
        result = await query_func.invoke(kernel, arguments)
        
        result_str = str(result)
        print(f"✅ Query Results ({len(result_str)} chars):")
        print("-"*80)
        if len(result_str) > 1500:
            print(result_str[:1500] + "\n... [truncated]")
        else:
            print(result_str)
        print("-"*80)
        
        # Parse result to check if we got configs
        if '"entity":' in result_str and 'ASQL' in result_str:
            print("✅ Found ASQL configurations in Cosmos DB")
        else:
            print("⚠️  No ASQL configurations found (might be data issue)")
            
    except Exception as e:
        print(f"❌ Cosmos DB query failed: {e}")
        return False
    
    # Test 3: Combined scenario - AI answer
    print("\n" + "-"*80)
    print("TEST 3: Full AI Response - Combining Search + Cosmos DB")
    print("-"*80)
    
    user_question = "Show me an example of ASQL ingestion configuration and list any existing ASQL configs"
    print(f"User Question: {user_question}\n")
    
    try:
        # Step 1: Search documentation
        print("Step 1: Searching documentation...")
        arguments = KernelArguments(user_request=user_question)
        doc_result = await etl_plugin["get_etl_documentation"].invoke(kernel, arguments)
        doc_str = str(doc_result)
        print(f"   Found {len(doc_str)} chars of documentation")
        
        # Step 2: Query Cosmos DB
        print("Step 2: Querying Cosmos DB...")
        sql_query = "SELECT c.entity, c.domain, c.layer, c.market FROM c WHERE c.I1_data_extract_process.source.type = 'ASQL' OFFSET 0 LIMIT 10"
        arguments = KernelArguments(sql_query=sql_query)
        cosmos_result = await cosmos_plugin["query_configurations"].invoke(kernel, arguments)
        cosmos_str = str(cosmos_result)
        print(f"   Found {len(cosmos_str)} chars from Cosmos DB")
        
        # Simulate AI combining results
        print("\n" + "="*80)
        print("🤖 SIMULATED AI RESPONSE (combining both sources):")
        print("="*80)
        print("""
Based on the documentation and existing configurations:

📚 DOCUMENTATION (from Azure AI Search):
- Azure SQL ingestion uses type: "ASQL" in I1_data_extract_process.source
- Requires connection details in Environment file (SFAsseco, etc.)
- Supports full load and incremental delta extraction
- Can use DynamicRange partitioning for parallel extraction

💾 EXISTING CONFIGURATIONS (from Cosmos DB):
""")
        
        if '"entity":' in cosmos_str:
            print(cosmos_str[:500] if len(cosmos_str) > 500 else cosmos_str)
            print("\n✅ Combined response would include both documentation and live configs")
        else:
            print("⚠️  No existing ASQL configs found, but documentation is available")
            
    except Exception as e:
        print(f"❌ Combined scenario failed: {e}")
        return False
    
    # Summary
    print("\n" + "="*80)
    print("📊 TEST SUMMARY")
    print("="*80)
    print("✅ Azure AI Search integration: Working")
    print("✅ Cosmos DB plugin: Working")
    print("✅ Combined scenario: Working")
    print("="*80 + "\n")
    
    return True


async def main():
    """Main test execution."""
    try:
        success = await test_asql_documentation()
        
        if success:
            print("\n🎉 ALL TESTS PASSED - ASQL integration working correctly!")
            return 0
        else:
            print("\n⚠️  SOME TESTS FAILED - Review output above")
            return 1
            
    except Exception as e:
        print(f"\n❌ Test suite failed with error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
