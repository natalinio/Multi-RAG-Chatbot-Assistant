"""
Test Azure AI Search - verify retrieval of I2 sink properties
"""
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
import os
from dotenv import load_dotenv

load_dotenv()

endpoint = os.getenv('AZURE_AI_SEARCH_ENDPOINT')
key = os.getenv('AZURE_AI_SEARCH_KEY')
index_name = os.getenv('AZURE_AI_SEARCH_INDEX_NAME', 'cpgai-gda-version')

client = SearchClient(endpoint=endpoint, index_name=index_name, credential=AzureKeyCredential(key))

print("\n" + "="*80)
print("TESTING AZURE AI SEARCH - I2 SINK PROPERTIES")
print("="*80)

# Test various queries
queries = [
    "I2_data_ingestion sink properties",
    "sink ADLS storage account file-format",
    "I2 ingestion sink configuration",
    "data ingestion sink type ADLS",
    "Bronze layer ingestion ADLS sink",
]

for query in queries:
    print(f"\n\nQuery: '{query}'")
    print("-" * 80)
    
    try:
        results = list(client.search(query, query_type="semantic", semantic_configuration_name="default", top=3))
        print(f"Found {len(results)} results:")
        
        for idx, result in enumerate(results, 1):
            print(f"\n{idx}. Entity: {result['entity']}")
            print(f"   Layer: {result['layer']}, Domain: {result['domain']}")
            print(f"   Source: {result['source']}")
            
            # Check if sink properties are in the content
            content = result['content']
            if 'sink' in content:
                print(f"   ✓ Contains 'sink' keyword")
            if 'storage-account' in content or 'storage_account' in content:
                print(f"   ✓ Contains storage account property")
            if 'I2_data_ingestion' in content:
                print(f"   ✓ Contains I2_data_ingestion block")
            
            # Show snippet
            print(f"   Snippet: {content[:150]}...")
    except Exception as e:
        print(f"Error: {e}")

print("\n" + "="*80)
